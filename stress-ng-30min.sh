#!/bin/bash

# Function to clean up background processes
cleanup() {
    echo "Cleaning up stress-ng processes..."
    pkill stress-ng
    echo "Cleanup completed"
    exit 0
}

# Check for cleanup command
if [ "$1" = "cleanup" ]; then
    cleanup
    exit 0
fi

# Check for required parameters
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <start_core> <end_core>"
    echo "To stop running tests: $0 cleanup"
    echo "Example: $0 1 4"
    exit 1
fi

# Validate input parameters
START=$1
END=$2

# Input validation
if ! [[ "$START" =~ ^[0-9]+$ ]] || ! [[ "$END" =~ ^[0-9]+$ ]]; then
    echo "Error: Please provide valid numbers for start and end cores"
    exit 1
fi

if [ "$START" -gt "$END" ]; then
    echo "Error: Start core number must be less than or equal to end core number"
    exit 1
fi

# Check if stress-ng is installed
if ! command -v stress-ng &> /dev/null; then
    echo "Error: stress-ng is not installed. Please install it first."
    exit 1
fi

# Start stress test on specified cores
echo "Starting stress test on cores $START to $END"
for (( i=START; i<=END; i++ )); do
    taskset -c "$i" stress-ng --ipsec-mb 1 2>/dev/null &
done

# Start timer in background
(
    sleep 1800  # Wait for 30 minutes
    echo "Stopping stress test..."
    pkill stress-ng &  # Kill stress-ng in background
    echo "Stress test completed"
) &

echo "Stress test is running in background"
echo "It will automatically stop after 30 minutes"
echo "You can continue using your terminal"
echo "To manually stop the test, run: $0 cleanup"
