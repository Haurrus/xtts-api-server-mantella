import ctypes
import uvicorn
from argparse import ArgumentParser
import os
import configparser
import sys

# Constants for console mode flags
ENABLE_QUICK_EDIT_MODE = 0x0040
ENABLE_EXTENDED_FLAGS  = 0x0080

def disable_quick_edit():
    """Disables Quick Edit Mode in the Windows CMD console."""
    kernel32 = ctypes.windll.kernel32
    hStdin = kernel32.GetStdHandle(-10)  # Get the standard input handle
    mode = ctypes.c_uint32()
    
    # Get the current console mode
    if not kernel32.GetConsoleMode(hStdin, ctypes.byref(mode)):
        raise ctypes.WinError()

    # Disable Quick Edit Mode and set the mode back
    mode.value &= ~ENABLE_QUICK_EDIT_MODE  # Unset the Quick Edit flag
    mode.value |= ENABLE_EXTENDED_FLAGS    # Make sure extended flags are enabled

    if not kernel32.SetConsoleMode(hStdin, mode):
        raise ctypes.WinError()
        
disable_quick_edit()

def clear_console():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def prompt_user_input(prompt, description, default):
    """Prompt the user for input with a description, then clean after the response."""
    print(f"{description}\n")  # Show the description first
    response = input(f"{prompt} [{default}]: ") or default  # Get the user's input
    clear_console()  # Clear the console after the input is provided
    return response

def create_config_file(config):
    """Create a config.ini file from user input."""
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def load_config_file():
    """Load configuration from config.ini if it exists."""
    config = configparser.ConfigParser()
    if os.path.exists('config.ini'):
        config.read('config.ini')
        return config
    return None

def ask_questions_and_create_config():
    """Ask questions to the user and create a configuration file."""
    config = configparser.ConfigParser()

    # Ask user for input with descriptions
    host = prompt_user_input("Host to bind", "This is the host address the server will bind to.", "localhost")
    port = prompt_user_input("Port to bind", "This is the port on which the server will listen.", "8020")
    device = prompt_user_input("Device (cpu/cuda)", "Choose 'cuda' for GPU usage or 'cpu' for CPU. Note: Using CUDA will consume up to 3 GB of GPU VRAM.", "cuda")
    speaker_folder = prompt_user_input("Speaker folder", "Folder containing speaker samples.", "speakers/")
    latent_speaker_folder = prompt_user_input("Latent speaker folder", "Folder containing latent speaker JSON data.", "latent_speaker_folder/")
    output = prompt_user_input("Output folder", "Folder where generated audio will be saved.", "output/")
    model_folder = prompt_user_input("Model folder", "Folder where models for XTTS will be stored.", "xtts_models/")
    version = prompt_user_input("Model version", "Specify which version of XTTS to use.", "v2.0.2")
    listen = prompt_user_input("Allow server to listen externally? (yes/no)", "Allow external access to the server.", "no").lower() == "yes"
    lowvram = prompt_user_input("Enable low VRAM mode? (yes/no)", "Optimize model for low VRAM usage.", "no").lower() == "yes"

    # Show a summarized GPU list before asking the DeepSpeed question
    print("\nDeepSpeed requires NVIDIA GPUs with CUDA support. Here are some examples of compatible GPUs:\n")

    print("- RTX 4000 Series (e.g., RTX 4090, RTX 4080, RTX 4070)")
    print("- RTX 3000 Series (e.g., RTX 3090, RTX 3080, RTX 3070, RTX 3060)")
    print("- RTX 2000 Series (e.g., RTX 2080 Ti, RTX 2070, RTX 2060)")
    print("- GTX 1000 Series (e.g., GTX 1080 Ti, GTX 1070, GTX 1060)")
    print("- TITAN Series (e.g., NVIDIA TITAN V, TITAN Xp, TITAN RTX)")
    print("- GTX 900 Series and older (e.g., GTX 980 Ti, GTX 970)")
    print("\nFor a full list of CUDA-compatible GPUs, visit: https://developer.nvidia.com/cuda-gpus\n")

    # Add DeepSpeed speedup information before asking the question
    print("Enabling DeepSpeed will significantly speed up processing (by 2 to 4 times) if you have a compatible GPU.\n")

    # Now prompt for the DeepSpeed question
    deepspeed = prompt_user_input("Enable DeepSpeed? (yes/no)", "Enable DeepSpeed for faster processing.", "no").lower() == "yes"

    # Add these values to the config parser
    config['DEFAULT'] = {
        'Host': host,
        'Port': port,
        'Device': device,
        'SpeakerFolder': speaker_folder,
        'LatentSpeakerFolder': latent_speaker_folder,
        'OutputFolder': output,
        'ModelFolder': model_folder,
        'ModelVersion': version,
        'Listen': str(listen).lower(),
        'LowVRAM': str(lowvram).lower(),
        'DeepSpeed': str(deepspeed).lower()
    }

    create_config_file(config)
    return config

def get_value_from_sources(arg_value, config_value, default_value):
    """Return the value based on the priority: arg_value > config_value > default_value"""
    if arg_value is not None:
        return arg_value
    elif config_value is not None:
        return config_value
    else:
        return default_value

def main():
    # Parse command-line arguments
    parser = ArgumentParser(description="Run the Uvicorn server.")
    parser.add_argument("-hs", "--host", help="Host to bind")
    parser.add_argument("-p", "--port", type=int, help="Port to bind")
    parser.add_argument("-d", "--device", help="Device that will be used (cpu/cuda)")
    parser.add_argument("-sf", "--speaker-folder", help="The folder where you get the samples for tts")
    parser.add_argument("-lsf", "--latent-speaker-folder", help="The folder where you get the latent in json format")
    parser.add_argument("-o", "--output", help="Output folder")
    parser.add_argument("-mf", "--model-folder", help="The place where models for XTTS will be stored.")
    parser.add_argument("-v", "--version", help="You can specify which version of xtts to use or specify your own model")
    parser.add_argument("--listen", action='store_true', help="Allow server to listen externally.")
    parser.add_argument("--lowvram", action='store_true', help="Enable low vram mode")
    parser.add_argument("--deepspeed", action='store_true', help="Enable DeepSpeed mode")
    args = parser.parse_args()

    # Load config.ini
    config = load_config_file()

    if config is None and len(sys.argv) <= 1:
        # If no config and no arguments, ask questions and create config.ini
        config = ask_questions_and_create_config()

    # Extract values, prioritizing command-line args > config.ini > hardcoded defaults
    host = get_value_from_sources(args.host, config.get('DEFAULT', 'Host', fallback=None) if config else None, "localhost")
    port = get_value_from_sources(args.port, config.getint('DEFAULT', 'Port', fallback=None) if config else None, 8020)
    device = get_value_from_sources(args.device, config.get('DEFAULT', 'Device', fallback=None) if config else None, "cuda")
    speaker_folder = get_value_from_sources(args.speaker_folder, config.get('DEFAULT', 'SpeakerFolder', fallback=None) if config else None, "speakers/")
    latent_speaker_folder = get_value_from_sources(args.latent_speaker_folder, config.get('DEFAULT', 'LatentSpeakerFolder', fallback=None) if config else None, "latent_speaker_folder/")
    output = get_value_from_sources(args.output, config.get('DEFAULT', 'OutputFolder', fallback=None) if config else None, "output/")
    model_folder = get_value_from_sources(args.model_folder, config.get('DEFAULT', 'ModelFolder', fallback=None) if config else None, "xtts_models/")
    version = get_value_from_sources(args.version, config.get('DEFAULT', 'ModelVersion', fallback=None) if config else None, "v2.0.2")
    listen = args.listen or (config.getboolean('DEFAULT', 'Listen', fallback=False) if config else False)
    lowvram = args.lowvram or (config.getboolean('DEFAULT', 'LowVRAM', fallback=False) if config else False)
    deepspeed = args.deepspeed or (config.getboolean('DEFAULT', 'DeepSpeed', fallback=False) if config else False)

    # Set environment variables based on the final values
    os.environ["LISTEN"] = str(listen).lower()
    host_ip = "0.0.0.0" if listen else host
    os.environ['DEVICE'] = device
    os.environ['OUTPUT'] = output
    os.environ['SPEAKER'] = speaker_folder
    os.environ['LATENT_SPEAKER'] = latent_speaker_folder
    os.environ['MODEL'] = model_folder
    os.environ['BASE_HOST'] = host_ip
    os.environ['BASE_PORT'] = str(port)
    os.environ['MODEL_VERSION'] = version
    os.environ['DEEPSPEED'] = str(deepspeed).lower()
    os.environ['LOWVRAM_MODE'] = str(lowvram).lower()

    # Run the uvicorn server
    from server import app
    uvicorn.run(app, host=host_ip, port=port)

if __name__ == "__main__":
    main()
