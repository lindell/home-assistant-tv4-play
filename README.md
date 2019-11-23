Home Assistant TV4 Play
----
![](https://github.com/lindell/home-assistant-tv4-play/workflows/Morning%20test/badge.svg)
![](https://github.com/lindell/home-assistant-tv4-play/workflows/Afternoon%20test/badge.svg)


Play tv4 play programs on home assistant media players.

Currently, only `tv4_play.play_suggested` is available, but the plan is to add more services.

## Installation

### Add the code

Copy the `custom_components/tv4_play` folder in this repository to `<home assistant config>/custom_components/tv4_play`

### Active the service

Add:
```yaml
tv4_play:
```
to your configuration.yaml file.

### Use in automations

And then add the automation you want:
```yaml
automation:
- alias:
  trigger:
  # Some trigger
  action:
  - service: tv4_play.play_suggested
    entity_id: media_player.living_room_tv
    data:
      program_name: nyhetsmorgon
```

## Get the `program_name` field

1. Search an click on the program you want at [tv4play.se](https://www.tv4play.se)
2. From the url, grab the name. It should be right after `program/`

![](https://share.lindell.me/2019/11/MassiveLeonberger.png)
