## Home Assistant TV4 Play

> [!NOTE]  
> As of 2023-11-29, TV4 changed their API which broke this integration. See [Issue#15](https://github.com/lindell/home-assistant-tv4-play/issues/15) for progress on making it work with the new API.

Play tv4 play programs on home assistant media players.

Currently, only `tv4_play.play_suggested` is available, but the plan is to add more services.

## Installation

### HACS (recommended)

1. Install [HACS (Home Assistant Community Store)](https://hacs.xyz/)
2. Go to HACS and install TV4 Play

### Manual

Copy the `custom_components/tv4_play` folder in this repository to `<home assistant config>/custom_components/tv4_play`

## Use

1. Add the integration through the integration tab in Home Assistant. See the [Get access token section](#get-access-token) for more details.
2. Use the services provided to play media.

## Get the program id

1. Search an click on the program you want at [tv4play.se](https://www.tv4play.se)
2. From the url, grab the name. It should be right after `program/`

![Get ID](https://github.com/user-attachments/assets/d46a9dca-1f37-4c8a-9908-c635a000b617)

## Get access token

These are instructions for Chrome, but the `tv4-refresh-token` cookie can be fetched from any other browser as well.

1. Go to [tv4play.se](https://www.tv4play.se)
2. Login
3. Go to the developer console

   ![Developer tools](https://github.com/user-attachments/assets/348f0c40-fde9-443e-a884-6551257c0848)

4. Application -> Cookies -> `https://tv4play.se`
5. In the list, select the value of tv4-refresh-token

![Select refresh token](https://github.com/user-attachments/assets/ad4574d4-6dd3-4b52-b9fd-6fabcb081ce4)
