# Finance Trade Strategies

Welcome to the Finance Trading Indicators Development and Testing Repository! This repository is designed to provide a comprehensive collection of Python scripts and tools for developing and testing finance trading indicators against both Stock and Crypto markets. Whether you are an experienced trader, a data scientist, or a Python enthusiast, this repository will empower you to build and evaluate custom trading indicators to enhance your trading strategies.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Supported Markets](#supported-markets)
- [Testing Strategies](#testing-strategies)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Trading indicators are essential tools used by traders to analyze price data and make informed trading decisions. This repository provides an extensive set of pre-built indicators as well as tools to develop and test custom indicators. Whether you are interested in simple moving averages or complex technical indicators like Bollinger Bands or MACD, this repository has got you covered. You can find my custom strategies under the [Strategies](./Strategies) project folder.

## Features

- A collection of popular pre-built trading indicators for quick analysis.
- Tools to develop and test custom trading indicators.
- Seamless integration with both Stock and Crypto market data.

## Installation

To get started with using the Finance Trading Indicators library, follow the steps below:

1. Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/finance-trade-strategies.git
```

2. Change into the repository directory:

```bash
cd finance-trade-strategies
```

3. Set up a virtual environment (recommended):

```bash
python -m venv venv
```

4. Activate the virtual environment:

On Windows:

```bash
venv\Scripts\activate
```

On macOS and Linux:

```bash
source venv/bin/activate
```

5. Install the required dependencies:

```bash
pip install -r requirements.txt
```

6. You're all set! Now you can start developing and testing your custom trading indicators.

## Usage

The main application provides supertrend & ADX finance strategies which are industry standards in quantitative finance analysis.
This doesn't guranteed positive profits rather a deep understanding on how frequency trading is done using bot applications.

### PseudoCode

1. check_adx -
2. tr, atr, supertrend - used to find super-trend on the indicators
3. check_buy_signals - takes adx & super-trend and determines the postion which should be held
4. run_bot - runs the perpertual data request from ccxt & populates the date-time series data - it then runs the data through the check_buy_signal and returns a json data that will be send as a notification to discord
5. main logic - an infinite loop that runs code then sleep for 60 seconds - runs adx logic the, sends adx to discord, prints adx dataframe - runs supertrend, sends supertrend data to discord
   ENDS

## Supported Markets

The ccxt library provides supports Crypto markets. It seamlessly integrates with popular market data providers, enabling you to access historical and real-time data for a wide range of assets.

## Testing Strategies

The `strategies` directory contains pre-built trading strategies that use the indicators from this library. You can use these strategies as a starting point and customize them to match your trading preferences.

## Contributing

Contributions to this repository are more than welcome! If you have any bug fixes, new features, or improvements, please open a pull request. Make sure to follow the guidelines mentioned in the CONTRIBUTING.md file.

## License

This repository is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code as permitted by the license.

---

We hope you find the Finance Trading Indicators Development and Testing Repository helpful in enhancing your trading strategies and exploring new market opportunities. Happy trading!

For any questions or support, please contact us at sinolewis@gmail.com
