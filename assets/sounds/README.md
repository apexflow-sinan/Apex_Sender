# Sound Files

This folder contains notification sounds for the application.

## Current Implementation

The application currently uses Windows system sounds via `winsound.MessageBeep()`:
- **Success**: `MB_OK` - System success sound
- **Error**: `MB_ICONHAND` - System error sound  
- **Notification**: `MB_ICONASTERISK` - System notification sound

## Custom Sounds (Optional)

To use custom sounds, place WAV files here:

- `success.wav` - Played on successful transfer
- `error.wav` - Played on transfer error
- `notification.wav` - Played on general notifications

### Requirements
- Format: WAV (PCM)
- Sample Rate: 44100 Hz recommended
- Channels: Mono or Stereo
- Duration: 1-2 seconds recommended

### Free Sound Resources
- [Freesound.org](https://freesound.org) - CC0 licensed sounds
- [Zapsplat.com](https://www.zapsplat.com) - Free sound effects
- [Mixkit.co](https://mixkit.co/free-sound-effects/) - Free sounds

## Implementation

The sound utility (`src/utils/sound_utils.py`) will automatically:
1. Check if custom WAV files exist
2. Use custom sounds if available
3. Fall back to system sounds if not

No code changes needed - just add the WAV files!
