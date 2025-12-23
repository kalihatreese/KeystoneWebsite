import time
import logging
from core import model
from workflow import orchestrator
from execution import executor, sandbox
from perception import file_watcher, web_fetcher, event_listener
from personality import voice_module
from config import settings, api_keys

# Logging setup
logging.basicConfig(
    filename="safety/action_log.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def initialize_system():
    logging.info("Initializing ReeseMirrorAI...")

    logging.info("Loading model...")
    ai_model = model.load_model(model_path="core/model/")
    tokenizer = model.load_tokenizer(tokenizer_path="core/tokenizer/")

    logging.info("Loading memory database...")
    memory_db = model.load_memory("core/memory.db")

    logging.info("Loading API keys...")
    keys = api_keys.load_keys("config/api_keys.py")

    logging.info("Loading user settings...")
    user_settings = settings.load("config/settings.json")

    logging.info("Initializing Veritas Reese voice module...")
    voice = voice_module.VeritasReese()

    orchestrator.init(ai_model, tokenizer, memory_db, voice, keys)
    executor.init(sandbox.Sandbox(), voice)

    file_watcher.init()
    web_fetcher.init()
    event_listener.init()

    logging.info("ReeseMirrorAI combined stub initialization complete.")
    return ai_model, tokenizer, memory_db, voice

def main_loop(ai_model, tokenizer, memory_db, voice):
    logging.info("Starting main loop...")
    try:
        cycle_count = 0
        while True:
            cycle_count += 1
            logging.info(f"Running cycle: {cycle_count}")
            orchestrator.run_cycle()

            fetched_files = web_fetcher.fetch()
            if fetched_files:
                voice.speak(f"Fetched {len(fetched_files)} files")
                logging.info(f"Veritas Reese: Fetched {len(fetched_files)} files")

            keys = api_keys.load_keys("config/api_keys.py")
            for api_name, api_key in keys.items():
                success = sandbox.safe_api_call(api_name, api_key)
                logging.info(f"Veritas Reese: Checked API {api_name}, success: {success}")
                voice.speak(f"Task 'Checking API {api_name}' executed successfully")

            orchestrator.run_plugins()
            model.save_memory("core/memory.db", orchestrator.memory)
            time.sleep(1)

    except KeyboardInterrupt:
        logging.info("Manual override triggered. Shutting down...")
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
    finally:
        logging.info("ReeseMirrorAI has stopped safely.")

if __name__ == "__main__":
    ai_model, tokenizer, memory_db, voice = initialize_system()
    voice.speak("Hello, ReeseMirrorAI is online.")
    main_loop(ai_model, tokenizer, memory_db, voice)
