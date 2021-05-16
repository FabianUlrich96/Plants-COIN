import serial


def main():
    global sample_number

    arduino_port = "COM5"
    baud = 9600
    file_name = input("File name: ")
    file_name = file_name + ".csv"
    while True:
        try:
            sample_number = int(input("Sample number to collect: "))
            break
        except ValueError:
            print("Please input integer only...")
            continue
    serial_port = serial.Serial(arduino_port, baud)

    print("Connected to Arduino port:" + arduino_port)
    file = open(file_name, "w")
    line = 0

    while line <= sample_number:
        getdata = serial_port.readline()
        data = getdata.decode('utf-8')
        print(data)
        file = open(file_name, "a")
        file.write(data)
        line = line + 1

    print("Data collection complete!")
    file.close()


if __name__ == '__main__':
    main()
