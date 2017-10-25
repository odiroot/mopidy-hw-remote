from signal import pause
from rotary import RotaryEncoderClickable, RotaryEncoder


#rotary = RotaryEncoderClickable(14, 15, 18, bounce_time=None)
rotary = RotaryEncoder(14, 15, bounce_time=2./1000)


def change(value):
    print(value)


rotary.when_rotated = change


def main():
    pause()


if __name__ == "__main__":
    main()
