# TV4 Play
Play tv4 play programs on home assistant media players.

Currently, only `tv4_play.play_suggested` is available, but the plan is to add more services.

## Configuration

### Active the service

Add the following to your config
```yaml
tv4_play:
```

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
