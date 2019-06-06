def main():
    while True:
        n = input('Height: ')
        try:
            if 0 < int(n) < 9:
                break
        except:
            continue
    pyramid(int(n))
    
def pyramid(n):
    for i in range(1, n + 1):
        print((n-i)*' ', i*'#', '', i*'#')
    
if __name__ == '__main__':
    main()