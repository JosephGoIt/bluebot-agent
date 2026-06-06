import os
import sys
import asyncio

if sys.platform == "win32":
    if sys.stdout is not None:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if sys.stderr is not None:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
from browser_use import Agent
from browser_use.llm.google.chat import ChatGoogle
from browser_use.browser.session import BrowserSession
import flet as ft

CONFIG_FILE = "config.txt"

def log_point(stage: str, details: str):
    """Utility function to output timestamped milestones to the terminal console."""
    print(f" LOG [{stage.upper()}]: {details}")

class VisualBrowser(BrowserSession):
    """BrowserSession subclass: forces visible Chrome and raises nav timeout to 20s."""
    def __init__(self, **kwargs):
        kwargs['headless'] = False
        chrome_exe = os.getenv("CHROME_PATH")
        if chrome_exe and os.path.exists(chrome_exe):
            kwargs['executable_path'] = chrome_exe
            kwargs['args'] = [
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--start-maximized",
            ]
        super().__init__(**kwargs)

    async def _navigate_and_wait(self, url, target_id, timeout=None, **kwargs):
        # Maersk and other heavy SPAs regularly exceed the default 8s cross-domain timeout
        if timeout is None:
            timeout = 20.0
        return await super()._navigate_and_wait(url, target_id, timeout=timeout, **kwargs)

def load_or_create_config():
    """Ensures a config file exists and loads keys/paths into the environment."""
    log_point("config", "Checking application directory for config.txt...")
    
    if getattr(sys, 'frozen', False):
        current_dir = os.path.dirname(sys.executable)
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
    config_path = os.path.join(current_dir, CONFIG_FILE)

    if not os.path.exists(config_path):
        log_point("config", f"Configuration file not found. Creating template at: {config_path}")
        with open(config_path, "w", encoding="utf-8") as f:
            f.write("# Bluebot Configuration File\n")
            f.write("# Replace placeholders with your actual credentials\n\n")
            f.write("GEMINI_API_KEY=your_gemini_api_key_here\n")
            f.write(r"CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe" + "\n")
        return False, config_path

    log_point("config", "Config file discovered. Reading parameters...")
    with open(config_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                clean_key = key.strip()
                clean_val = val.strip()
                
                os.environ[clean_key] = clean_val
                if clean_key == "GEMINI_API_KEY":
                    os.environ["GOOGLE_API_KEY"] = clean_val
                    
    log_point("config", "Environment configurations successfully loaded.")
    return True, config_path


def main(page: ft.Page):
    log_point("ui_init", "Initializing Flet application environment...")
    page.title = "Bluebot Automation Client"
    page.window_width = 550
    page.window_height = 650
    page.window_resizable = False
    page.padding = 25
    page.theme_mode = ft.ThemeMode.DARK

    config_found, path_to_config = load_or_create_config()

    instruction_input = ft.TextField(
        label="Task Instructions",
        hint_text="Enter your specific cargo tracking guidelines...",
        multiline=True,
        min_lines=4,
        max_lines=6,
        expand=True,
    )
    
    status_label = ft.Text("Ready", size=14, color="bluegrey400")

    result_box = ft.TextField(
        label="Agent Result",
        multiline=True,
        min_lines=4,
        max_lines=10,
        read_only=True,
        expand=True,
        visible=False,
    )

    run_button = ft.Button(
        content="Execute Task", 
        icon="play_arrow", 
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
        height=50
    )

    api_key = os.getenv("GOOGLE_API_KEY")
    if not config_found or not api_key or "your_gemini_api_key" in api_key:
        log_point("security", "Application UI locked due to placeholder key parameters.")
        instruction_input.disabled = True
        run_button.disabled = True
        status_label.value = f"⚠️ Action Required: Please update details inside:\n{path_to_config}"
        status_label.color = "amber400"
    

    async def execute_agent_workflow(task_prompt):
        try:
            log_point("llm_setup", "Initializing ChatGoogle (native browser-use LLM)...")
            llm = ChatGoogle(
                model="gemini-2.5-flash",
                api_key=os.getenv("GOOGLE_API_KEY")
            )

            log_point("browser_runtime", "Spawning validated Custom Visual Browser application...")
            status_label.value = "🌐 Launching your physical Google Chrome application panel..."
            page.update()

            browser_instance = VisualBrowser()

            log_point("agent_setup", "Instantiating browser-use agent thread mapping...")
            agent = Agent(
                task=task_prompt,
                llm=llm,
                browser_session=browser_instance
            )
            
            log_point("browser_runtime", "Chrome viewport context online. Handing off tracking instructions...")
            status_label.value = "🚀 Tracking sequence active. Watch your screen..."
            page.update()
            
            result = await agent.run()
            
            log_point("browser_runtime", f"Automation sequence completed. Details: {result}")
            final = result.final_result()
            result_box.value = final if final else str(result)
            result_box.visible = True
            status_label.value = "✅ Task completed successfully!"
            status_label.color = "green400"
            
        except Exception as ex:
            log_point("runtime_error", f"CRITICAL CRASH DETECTED: {str(ex)}")
            status_label.value = f"❌ Error: {str(ex)}"
            status_label.color = "red400"
            
        finally:
            log_point("execution", "Re-enabling interface panels for subsequent runs.")
            instruction_input.disabled = False
            run_button.disabled = False
            page.update()


    def run_button_clicked(e):
        task_prompt = instruction_input.value.strip()
        if not task_prompt:
            status_label.value = "⚠️ Please enter an instruction first."
            status_label.color = "red400"
            page.update()
            return

        log_point("execution", "User triggered automation sequence.")
        instruction_input.disabled = True
        run_button.disabled = True
        result_box.value = ""
        result_box.visible = False
        status_label.value = "🤖 Bluebot Agent is starting up..."
        status_label.color = "blue200"
        page.update()

        asyncio.create_task(execute_agent_workflow(task_prompt))

    run_button.on_click = run_button_clicked

    page.add(
        ft.Column(
            controls=[
                ft.Text("Bluebot Agent", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Enter your command below to activate the autonomous automation engine.", size=13, color="bluegrey300"),
                ft.Divider(height=20, color="surfacevariant"),
                instruction_input,
                ft.Container(height=10),
                ft.Row([run_button], alignment=ft.MainAxisAlignment.END),
                ft.Divider(height=20, color="surfacevariant"),
                ft.Text("System Status:", size=12, weight=ft.FontWeight.W_500),
                status_label,
                result_box
            ],
            expand=True
        )
    )

if __name__ == "__main__":
    ft.run(main)