import smbus
import time

# I2C address of the MPU-6050 (0x68 or 0x69 depending on the AD0 pin)
MPU_ADDR = 0x68

# Initialize the I2C bus (use 1 for /dev/i2c-1)
I2C_BUS_NUMBER = 1
bus = smbus.SMBus(I2C_BUS_NUMBER)

def read_word_2c(register):
    high_byte = bus.read_byte_data(MPU_ADDR, register)
    low_byte = bus.read_byte_data(MPU_ADDR, register + 1)
    value = (high_byte << 8) + low_byte
    if value >= 0x8000:
        return -((65535 - value) + 1)
    else:
        return value

def convert_int16_to_str(i):
    return "{:6d}".format(i)

def read_sensor_data():
    accelerometer_x = read_word_2c(0x3B)
    accelerometer_y = read_word_2c(0x3D)
    accelerometer_z = read_word_2c(0x3F)
    temperature = read_word_2c(0x41)
    gyro_x = read_word_2c(0x43)
    gyro_y = read_word_2c(0x45)
    gyro_z = read_word_2c(0x47)
    return accelerometer_x, accelerometer_y, accelerometer_z, temperature, gyro_x, gyro_y, gyro_z

def main():
    bus.write_byte_data(MPU_ADDR, 0x6B, 0)  # Wake up the MPU-6050

    while True:
        accelerometer_x, accelerometer_y, accelerometer_z, temperature, gyro_x, gyro_y, gyro_z = read_sensor_data()

        print("aX = {} | aY = {} | aZ = {} | tmp = {:.2f} | gX = {} | gY = {} | gZ = {}".format(
            convert_int16_to_str(accelerometer_x),
            convert_int16_to_str(accelerometer_y),
            convert_int16_to_str(accelerometer_z),
            temperature / 340.0 + 36.53,
            convert_int16_to_str(gyro_x),
            convert_int16_to_str(gyro_y),
            convert_int16_to_str(gyro_z)
        ))

        time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        bus.close()
