# Tildes Balss TTS 
Tildes Balss Text-to-Speech platform for Home Assistant.

## Installation
Download the [latest release](https://github.com/girtskokars/hass-tildes-balss/releases/latest).
Unpack the release and copy the custom_components/tildes_balss directory into the custom_components directory of your Home Assistant installation.
Add/configure the tildes_balss platform.
Restart Home Assistant.

## Configuration
```yaml
tts:
  - platform: tildes_balss
```

## Usage
```yaml
- service: tts.tildes_balss_say
  data:
    message: 'Sveika pasaule'
```