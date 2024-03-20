~~This project has a GUI where you set a list of `n` dice each with `x` sides then use mouse activity to generate randomness which is used to determine the rolls.~~

This is a command line program for rolling dice.  
The dice rolls are generated, in part, using your mouse movments to make it feel more like actually rolling dice.

The program takes in args in the following format `<number>d<sides>[,<keep>][,<group_copies>]`  
`<number>` is the number of dice to roll  
`<sides>` is the number of sides on the dice  
`<keep>` is the number of dice to keep  
`<group_copies>` is the number of times to roll the group of dice  
You can pass in multiple dice groups at a time sperated by a space. `./cli_dice.exe 4d6 1d20`  

You can also use the `-i` flag to read in a yaml file to reroll the same dice from your previous roll.  
Optionally you can lock in the values of some of the rolls.

### Lets look at some examples:

#### You want to generate Ability Scores for a DnD character:
`./cli_dice.exe 4d6,3,6`  
`4d6` You want 4 six sided dice (This will be enough to calculate one ability score).  
`3` you only want to keep the values of the top 3 roles  
`6` you want `4d6,3` 6 times for each ability score.  
Your output would look like this:  
```
┏━━━━━━━┳━━━━━━┳━━━━┳━━━━━━━┳━━━━━━┳━━━━┳━━━━━━━┳━━━━━━┳━━━━┳━━━━━━━┳━━━━━━┳━━━━┳━━━━━━━┳━━━━━━┳━━━━┳━━━━━━━┳━━━━━━┳━━━━┳━━━━━━━┳━━━━━━━━━━━━┓
┃ d6    ┃ roll ┃ k3 ┃ d6    ┃ roll ┃ k3 ┃ d6    ┃ roll ┃ k3 ┃ d6    ┃ roll ┃ k3 ┃ d6    ┃ roll ┃ k3 ┃ d6    ┃ roll ┃ k3 ┃ Total ┃ Keep Total ┃
┡━━━━━━━╇━━━━━━╇━━━━╇━━━━━━━╇━━━━━━╇━━━━╇━━━━━━━╇━━━━━━╇━━━━╇━━━━━━━╇━━━━━━╇━━━━╇━━━━━━━╇━━━━━━╇━━━━╇━━━━━━━╇━━━━━━╇━━━━╇━━━━━━━╇━━━━━━━━━━━━┩
│ 1     │ 4    │ -  │ 1     │ 1    │ -  │ 1     │ 2    │ -  │ 1     │ 6    │ -  │ 1     │ 4    │ -  │ 1     │ 5    │ -  │ 80    │ 70         │
│ 2     │ 2    │ -  │ 2     │ 6    │ -  │ 2     │ 2    │ -  │ 2     │ 3    │ -  │ 2     │ 2    │ -  │ 2     │ 6    │ -  │       │            │
│ 3     │ 4    │ -  │ 3     │ 1    │ -  │ 3     │ 1    │ -  │ 3     │ 2    │ -  │ 3     │ 2    │ -  │ 3     │ 3    │ -  │       │            │
│ 4     │ 5    │ -  │ 4     │ 5    │ -  │ 4     │ 5    │ -  │ 4     │ 5    │ -  │ 4     │ 2    │ -  │ 4     │ 2    │ -  │       │            │
│ Total │ 15   │ 13 │ Total │ 13   │ 12 │ Total │ 10   │ 9  │ Total │ 16   │ 14 │ Total │ 10   │ 8  │ Total │ 16   │ 14 │       │            │
└───────┴──────┴────┴───────┴──────┴────┴───────┴──────┴────┴───────┴──────┴────┴───────┴──────┴────┴───────┴──────┴────┴───────┴────────────┘
```
Netting you the following roll values:  
13,12,9,14,8,14

#### You want to roll a d20 to see if you hit a target:
`./cli_dice.exe 1d20`  
`1d20` You want 1 twenty sided dice  
Your output would look like this:  
```
┏━━━━━━━┳━━━━━━┳━━━━┳━━━━━━━┳━━━━━━━━━━━━┓
┃ d20   ┃ roll ┃ k1 ┃ Total ┃ Keep Total ┃
┡━━━━━━━╇━━━━━━╇━━━━╇━━━━━━━╇━━━━━━━━━━━━┩
│ 1     │ 20   │ -  │ 20    │ 20         │
│ Total │ 20   │ 20 │       │            │
└───────┴──────┴────┴───────┴────────────┘
```

#### Yahtzee:
`./cli_dice.exe 5d6`  
`5d6` You want 5 six sided dice  
Now lets say you want to keep the 3 highest rolls rerolling the other 2  
Your first command generates a dice.yaml file that can be modified to lock in the dice you want to keep.  
`./cli_dice.exe -i dice.yaml` will read in your previous rolls and only reroll the dice you didn't lock in.  
```yaml
- dice:
  - 1_value: 1
    2_locked: false
  - 1_value: 3
    2_locked: false # set to true
  - 1_value: 4
    2_locked: false # set to true
  - 1_value: 1
    2_locked: false
  - 1_value: 3
    2_locked: false # set to true
  keep: 5
  sides: 6
```
Lets keep the 3 highest rolls by setting `locked` to `true` and reroll the other 2 dice  
**Before:**
```yaml
- dice:
  - 1_value: 1
    2_locked: false
  - 1_value: 3
    2_locked: true
  - 1_value: 4
    2_locked: true
  - 1_value: 1
    2_locked: false
  - 1_value: 3
    2_locked: true
  keep: 5
  sides: 6
```
`./cli_dice.exe -i dice.yaml`  
**After**
```yaml
- dice:
  - 1_value: 4
    2_locked: false
  - 1_value: 3
    2_locked: true
  - 1_value: 4
    2_locked: true
  - 1_value: 3
    2_locked: false
  - 1_value: 3
    2_locked: true
  keep: 5
  sides: 6
```
We went from:
`1,3,4,1,3` to `4,3,4,3,3`



### Notes
Potential ideas for dice?
https://stackoverflow.com/a/45226554

https://github.com/gsempe/diceware/wiki/Diceware-Password-Generator-How-It-Works

mouseCollector
https://github.com/gsempe/diceware/blob/master/diceware-server/public/js/main.js#L141-L157