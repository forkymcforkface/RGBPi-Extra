# title: Arcade Freeplay Mode
# description: Enables free play mode for arcade games, bypassing coin insertion.
# info: No coins needed!

def status
grep -q "free_play = on" "$RTK_CFG_FILE"

def on
sed -i 's/free_play = off/free_play = on/' "$RTK_CFG_FILE"

def off
sed -i 's/free_play = on/free_play = off/' "$RTK_CFG_FILE"
