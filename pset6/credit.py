def main():
    while True:
        card_no = input("Enter card number: ")
        try:
            if type(int(card_no)) == int:
                luhn_algo(card_no)
                break
        except:
            continue

def luhn_algo(card_no):
    final_sum = 0
    for i in range(-1, -len(card_no)-1, -1):
        if i % 2 == 0:
            product = 2*(int(card_no[i]))
            final_sum += product // 10
            final_sum += product % 10
        else:
            final_sum += int(card_no[i])

    check = final_sum % 10
    amex_valid = [34, 37]
    master_valid = [51, 52, 53, 54, 55]
    visa_lens = [13, 16]
    
    if (check == 0) and (len(card_no) == 15) and (int(card_no[0:2]) in amex_valid):
        print('AMEX')
    elif (check == 0) and (len(card_no) == 16) and (int(card_no[0:2]) in master_valid):
        print('MASTERCARD')
    elif (check == 0) and (len(card_no) in visa_lens) and (int(card_no[0]) == 4):
        print('VISA')
    else:
        print('INVALID')

if __name__ == '__main__':
    main()