Home Assistant TV4 Play
----

Play tv4 play programs on home assistant.

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
