#!/bin/bash

# Navigate to the directory where you want to store the csv file
cd /home/GuilhemDavignonAllo/Project

# Get the current price of Bitcoin from Coingecko using curl and grep
PRICE=$(curl 'https://www.coingecko.com/en/coins/bitcoin' | grep -oP '(?<=USD \$)[0-9,.]+' | tr -d ',' | head -1)

# Get the current date and time
DATE=$(date +"%Y-%m-%d %H:%M:%S")

# Append the price and date to the csv file
echo "$DATE,$PRICE" >> data.csv
