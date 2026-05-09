import os
import pyautogui
import psutil
import win32gui
import win32process
import google.generativeai as genai
from openai import OpenAI
import base64
from dotenv import load_dotenv

load_dotenv()


class AdaptixCollector:
    def __init__(self, api_key=None, provider="gemini"):
        self.provider = provider.lower()
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

        Task:
        1. Identify exactly what the user is doing.
        2. Categorize this behavior (e.g., Coding, Browsing, Gaming, Social).
        3. Note any potential 'habits' if this were a repeated action.
        Keep it concise (1 sentence).
        """

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
        1. Summarize the user's main activities during this session.
        2. Based on these habits, describe what kind of person this user seems to be (e.g., focused developer, multi-tasking researcher, easily distracted, etc.).
        3. Provide one piece of advice to improve their productivity based on these habits.

        Be insightful and a bit psychological.
        """

        if self.provider == "gemini":
            response = self.model.generate_content(prompt)
            return response.text
        elif self.provider == "openai":
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
            )
            return response.choices[0].message.content
        return "Unknown provider."


if __name__ == "__main__":
    collector = AdaptixCollector()
    print("Capturing context...")
    print(collector.analyze_behavior())
