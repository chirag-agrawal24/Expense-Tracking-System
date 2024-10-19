import subprocess
import time
import os
import signal

# Define the commands to run FastAPI and Streamlit with directory paths
def run_fastapi():
    # Change directory to 'backend' and run FastAPI (assuming it's using Uvicorn)
    os.chdir("../backend")
    return subprocess.Popen(["uvicorn", "server:app", "--reload"])

def run_streamlit():
    # Change directory to 'frontend' and run Streamlit
    os.chdir("../frontend")
    return subprocess.Popen(["streamlit", "run", "app.py"])

if __name__ == "__main__":
    try:
        # Start FastAPI in a subprocess
        fastapi_process = run_fastapi()

        # Start Streamlit in a subprocess
        streamlit_process = run_streamlit()

        # Keep the main program running until interrupted
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        # If the user presses Ctrl+C, terminate both processes
        print("Terminating FastAPI and Streamlit...")
        fastapi_process.terminate()
        streamlit_process.terminate()
    
    finally:
        # Ensure both subprocesses are terminated properly
        fastapi_process.kill()
        streamlit_process.kill()
        print("Both FastAPI and Streamlit have been terminated.")
