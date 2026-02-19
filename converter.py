#!/usr/bin/env python3
"""
Engineering Unit Converter
Converts between common industrial automation units.
"""

import argparse
import sys


def convert_pressure(value, from_unit, to_unit):
    """Convert pressure between psi, bar, kPa, MPa."""
    # Convert to Pa first
    to_pa = {
        'psi': 6894.757,
        'bar': 100000,
        'kpa': 1000,
        'mpa': 1000000,
        'pa': 1
    }
    
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    if from_unit not in to_pa or to_unit not in to_pa:
        raise ValueError(f"Unsupported pressure units. Use: {', '.join(to_pa.keys())}")
    
    pa_value = value * to_pa[from_unit]
    return pa_value / to_pa[to_unit]


def convert_temperature(value, from_unit, to_unit):
    """Convert temperature between C, F, K."""
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    
    valid_units = ['c', 'celsius', 'f', 'fahrenheit', 'k', 'kelvin']
    if from_unit not in valid_units or to_unit not in valid_units:
        raise ValueError(f"Unsupported temperature units. Use: c, f, k")
    
    # Normalize unit names
    from_unit = from_unit[0]  # Just use first letter
    to_unit = to_unit[0]
    
    # Convert to Celsius first
    if from_unit == 'c':
        celsius = value
    elif from_unit == 'f':
        celsius = (value - 32) * 5/9
    elif from_unit == 'k':
        celsius = value - 273.15
    
    # Convert from Celsius to target
    if to_unit == 'c':
        return celsius
    elif to_unit == 'f':
        return (celsius * 9/5) + 32
    elif to_unit == 'k':
        return celsius + 273.15


def convert_flow(value, from_unit, to_unit):
    """Convert flow between gpm, lpm, m3/h."""
    # Convert to lpm first
    to_lpm = {
        'gpm': 3.78541,
        'lpm': 1,
        'm3h': 16.6667,
        'm3/h': 16.6667
    }
    
    from_unit = from_unit.lower().replace('/', '')
    to_unit = to_unit.lower().replace('/', '')
    
    if from_unit not in to_lpm or to_unit not in to_lpm:
        raise ValueError(f"Unsupported flow units. Use: gpm, lpm, m3h (or m3/h)")
    
    lpm_value = value * to_lpm[from_unit]
    return lpm_value / to_lpm[to_unit]


def main():
    parser = argparse.ArgumentParser(
        description='Engineering Unit Converter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s pressure 100 psi bar      # Convert 100 psi to bar
  %(prog)s temp 212 f c              # Convert 212°F to Celsius
  %(prog)s flow 50 gpm m3h           # Convert 50 gpm to m³/h
        """
    )
    
    parser.add_argument('type', choices=['pressure', 'temp', 'flow'],
                        help='Type of conversion')
    parser.add_argument('value', type=float, help='Value to convert')
    parser.add_argument('from_unit', help='Source unit')
    parser.add_argument('to_unit', help='Target unit')
    
    args = parser.parse_args()
    
    try:
        if args.type == 'pressure':
            result = convert_pressure(args.value, args.from_unit, args.to_unit)
            print(f"{args.value} {args.from_unit} = {result:.4f} {args.to_unit}")
        
        elif args.type == 'temp':
            result = convert_temperature(args.value, args.from_unit, args.to_unit)
            print(f"{args.value}°{args.from_unit.upper()} = {result:.2f}°{args.to_unit.upper()}")
        
        elif args.type == 'flow':
            result = convert_flow(args.value, args.from_unit, args.to_unit)
            print(f"{args.value} {args.from_unit} = {result:.4f} {args.to_unit}")
    
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    # Quick self-test
    if len(sys.argv) == 1:
        print("Running self-test...")
        print()
        
        # Pressure tests
        assert abs(convert_pressure(100, 'psi', 'bar') - 6.8948) < 0.001
        assert abs(convert_pressure(1, 'bar', 'kpa') - 100) < 0.001
        print("✓ Pressure conversions work")
        
        # Temperature tests
        assert abs(convert_temperature(212, 'f', 'c') - 100) < 0.01
        assert abs(convert_temperature(0, 'c', 'k') - 273.15) < 0.01
        print("✓ Temperature conversions work")
        
        # Flow tests
        assert abs(convert_flow(1, 'gpm', 'lpm') - 3.78541) < 0.001
        assert abs(convert_flow(1, 'm3h', 'lpm') - 16.6667) < 0.001
        print("✓ Flow conversions work")
        
        print()
        print("All tests passed! 🎉")
        print()
        print("Usage examples:")
        print("  python converter.py pressure 100 psi bar")
        print("  python converter.py temp 212 f c")
        print("  python converter.py flow 50 gpm m3h")
        sys.exit(0)
    
    main()
