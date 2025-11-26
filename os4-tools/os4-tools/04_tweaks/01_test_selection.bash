# title: Test Selection
# description: A test script for multi-selection
# type: selection
# options: Option 1, Option 2, Option 3
# default: Option 2

def option_1
    echo "You selected Option 1" >> /tmp/selection_test.log

def option_2
    echo "You selected Option 2" >> /tmp/selection_test.log

def option_3
    echo "You selected Option 3" >> /tmp/selection_test.log

def status
    # This is optional if we rely on config, but good for testing
    # echo "Option 1"
    pass
