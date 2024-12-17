import threading
import time
import random

# Shared event for signaling the interrupt
interrupt_event = threading.Event()

# Simulated function for playing audio
def audio_playback(response, playback_id):
    print(f"Thread-{playback_id}: Starting audio playback: '{response}'")
    for i, word in enumerate(response.split()):
        if interrupt_event.is_set():  # Check if interrupt event is triggered
            print(f"Thread-{playback_id}: Interrupted at word '{word}'!")
            interrupt_event.clear()  # Reset the interrupt
            return
        print(f"Thread-{playback_id}: Playing word: '{word}'")
        time.sleep(0.5)  # Simulate audio playback time
    print(f"Thread-{playback_id}: Playback complete.")

# Simulated function for predicting an interrupt point
def predictor(response, playback_id, trigger_word):
    print(f"Interruptor: Monitoring playback-{playback_id}...")
    words = response.split()
    # Predict when to send an interrupt
    for i, word in enumerate(words):
        if word == trigger_word:
            print(f"Interruptor: Interrupt predicted at word '{word}'!")
            time.sleep(i * 0.5)  # Wait until that point in playback
            interrupt_event.set()  # Trigger the interrupt
            return
    print("Interruptor: No trigger word found, no interrupt sent.")

# Thread for audio input simulation (listening to audio)
def audio_listener():
    print("Listener: Listening to audio input...")
    while True:
        time.sleep(random.uniform(1, 3))  # Simulate random listening events
        print("Listener: Heard something interesting!")

# Main function to simulate the threading
def main():
    # Sample responses from ChatGPT
    responses = [
        "Hello there how are you doing today",
        "The quick brown fox jumps over the lazy dog",
        "Python is a versatile programming language"
    ]
    trigger_word = "jumps"  # Word at which the interrupt occurs
    
    # Start the audio listener thread
    listener_thread = threading.Thread(target=audio_listener, daemon=True)
    listener_thread.start()

    # Start the audio playback threads with interrupt prediction
    for i, response in enumerate(responses):
        playback_thread = threading.Thread(target=audio_playback, args=(response, i))
        predictor_thread = threading.Thread(target=predictor, args=(response, i, trigger_word))
        
        playback_thread.start()
        predictor_thread.start()
        
        playback_thread.join()
        predictor_thread.join()

if __name__ == "__main__":
    main()