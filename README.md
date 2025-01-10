## Home Assistant TV4 Play

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

## Get access token

These are

1. Go to [tv4play.se](https://www.tv4play.se)
2. Login
3. Go to the developer console

   ![Developer tools](https://github.com/user-attachments/assets/348f0c40-fde9-443e-a884-6551257c0848)

4. Application -> Cookies -> `https://tv4play.se`
5. In the list, select the value of tv4-refresh-token

![Select refresh token](https://github.com/user-attachments/assets/c79041cb-7a64-4a01-8191-1c865a67105f)
