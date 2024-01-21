# Tire Code Parser

## Description
Tire Code Parser is a Python tool designed to parse various tire specifications from tire codes. It's a work in progress and under testing.

## Features
- Parses tire specifications from various formats.
- Extractable specs include:
  - SERVICE_TYPE
  - TIRE_WIDTH
  - ASPECT_RATIO
  - WHEEL_DIAMETER
  - OVERALL_DIAMETER
  - LOAD_INDEX
  - LOAD_INDEX_DUAL
  - SPEED_RATING

## Example
For a tire code like "215/70R16 100T", the tool extracts and provides the detailed specs.

## Usage
To use the Tire Code Parser, simply pass your tire code string to the `TireCode` object:

```python
parsed_tire_code = TireCode("your_tire_code")
print(parsed_tire_code.specs.TIRE_WIDTH)
print(parsed_tire_code.specs.WHEEL_DIAMETER)
```

You can also access all spec values as a dictionary:

```python
parsed_tire_code.specs_dict
```

## Contributing
Any suggestions or contributions are welcome! I hope you find this package useful.

## License
MIT License
