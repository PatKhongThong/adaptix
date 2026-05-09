import os
import pyautogui
import psutil
import win32gui
import win32process
import google.generativeai as genai
from openai import OpenAI
import base64
import json
from dotenv import load_dotenv

load_dotenv()


class AdaptixCollector:
    def __init__(self, api_key=None, provider="gemini"):
        self.provider = provider.lower()
        self.memory_path = "D:\\temp\\adaptix_memory.json"
        self.memory = self.load_memory()

        if self.provider == "gemini":
            self.api_key = api_key or os.getenv("GEMINI_API_KEY")
            if self.api_key:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.0-flash')
            else:
                self.model = None
        elif self.provider == "openai":
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            if self.api_key:
                self.client = OpenAI(api_key=self.api_key)
            else:
                self.client = None

        # Ensure temp directory for captures exists on D:
        self.temp_dir = "D:\\temp\\adaptix_captures"
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

        # State for minimizing API usage
        self.last_screenshot = None
        self.last_window_title = None
        self.change_threshold = 5.0  # Percentage of pixels that must change

    def get_active_window_info(self):
        try:
            window = win32gui.GetForegroundWindow()
            title = win32gui.GetWindowText(window)
            _, pid = win32process.GetWindowThreadProcessId(window)
            process = psutil.Process(pid)
            exe = process.name()
            return {"title": title, "app": exe}
        except Exception:  # pylint: disable=broad-exception-caught
            return {"title": "Unknown", "app": "Unknown"}

    def load_memory(self):
        try:
            if os.path.exists(self.memory_path):
                with open(self.memory_path, "r") as f:
                    return json.load(f)
        except Exception:
            pass
        return {"sessions": [], "long_term_habits": "User is new."}

    def save_to_memory(self, session_data, summary):
        import time
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.memory["sessions"].append({
            "timestamp": timestamp,
            "summary": summary
        })
        # Keep the last 20 sessions for history browsing
        self.memory["sessions"] = self.memory["sessions"][-20:]
        self.memory["long_term_habits"] = summary
        
        try:
            with open(self.memory_path, "w") as f:
                json.dump(self.memory, f)
        except Exception:
            pass

    def has_changed(self, current_img, current_window_title):
        # 1. Window Change is a guaranteed "interesting" event
        if current_window_title != self.last_window_title:
            return True, "Window changed"

        # 2. Image Change Detection
        if self.last_screenshot is None:
            return True, "Initial capture"

        # Resize both to small thumbnails for very fast comparison
        size = (64, 64)
        img1 = self.last_screenshot.resize(size).convert('L')
        img2 = current_img.resize(size).convert('L')

        # Calculate difference (RMSE)
        import math
        import operator
        from functools import reduce

        # Simple pixel difference check
        diff = math.sqrt(reduce(operator.add, map(lambda a, b: (a - b)**2, img1.getdata(), img2.getdata())) / (size[0] * size[1]))
        
        if diff > self.change_threshold:
            return True, f"Screen changed (diff: {diff:.2f})"

        return False, "No significant change"

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_behavior(self):
        window_info = self.get_active_window_info()
        screenshot = pyautogui.screenshot()
        
        changed, reason = self.has_changed(screenshot, window_info['title'])
        
        # Update state
        self.last_screenshot = screenshot
        self.last_window_title = window_info['title']
        
        if not changed:
            return f"SKIP: {reason}"

        # If changed, proceed to AI analysis
        # Resize for faster processing and lower token usage
        screenshot.thumbnail((1280, 720))
        path = os.path.join(self.temp_dir, "last_capture.png")
        screenshot.save(path)

        prompt = f"""
        Analyze this computer activity.
        Active App: {window_info['app']}
        Window Title: {window_info['title']}
        
        Long-term Habits (Memory):
        {self.memory.get('long_term_habits', 'No history yet.')}

        Task:
        1. Inspect the CONTENTS of the active window (e.g., search queries, specific messages, video titles, code snippets).
        2. Identify exactly what the user is doing and the context (e.g., "Searching for React hooks on Google", "Messaging a friend about lunch").
        3. Compare this to their known long-term habits.
        Keep it concise (1 sentence).
        """
        
        # Use the full screenshot for detail
        if self.provider == "gemini":
            if not self.model:
                return "Gemini API Key not configured."
            response = self.model.generate_content([prompt, screenshot])
            return response.text

        elif self.provider == "openai":
            if not self.client:
                return "OpenAI API Key not configured."
            base64_image = self.encode_image(path)
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )
            return response.choices[0].message.content

        return "Unknown provider."

    def summarize_session(self, insights):
        if not insights:
            return "No data collected."

        combined_text = "\n".join(insights)
        prompt = f"""
        Below is a log of AI-analyzed behavior from a computer usage session.

        Log:
        {combined_text}

        Task:
        Provide a simple and friendly summary of this session. 
        Focus on the positive aspects of the user's workflow:
        1. **What you achieved**: A quick, 2-3 sentence summary of the main things they got done.
        2. **Your Strengths**: Highlight 2-3 things the user is good at based on their focus (e.g., "Great at staying focused on code", "Very organized researcher").
        3. **Friendly Tip**: One small, encouraging suggestion to help them even more.
        
        Avoid any negative or judgmental language. Keep it simple, clear, and very encouraging.
        """

        if self.provider == "gemini":
            response = self.model.generate_content(prompt)
            result = response.text
        elif self.provider == "openai":
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
            )
            result = response.choices[0].message.content
        else:
            result = "Unknown provider."

        # Save to memory
        self.save_to_memory(insights, result)
        return result


if __name__ == "__main__":
    collector = AdaptixCollector()
    print("Capturing context...")
    print(collector.analyze_behavior())
