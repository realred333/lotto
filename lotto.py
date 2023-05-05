import random
import csv

# csv 파일에서 당첨번호 가져오기
with open('lotto_win_nums.csv', newline='') as f:
    reader = csv.reader(f)
    win_nums = []
    for row in reader:
        win_nums.append(list(map(int, row[:6])))

# 이월수 구하기
def get_carryover_num(win_nums):
    carryover_num = [0] * 45
    for nums in win_nums:
        for num in nums:
            carryover_num[num-1] += 1
    return carryover_num

# 역수 구하기
def get_reverse_num(win_nums):
    reverse_num = [0] * 45
    for nums in win_nums:
        for num in nums:
            reverse_num[45-num] += 1
    return reverse_num

'''
# 최근 24회차까지의 번호 출현 횟수 구하기
def get_recent_num_counts(win_nums):
    recent_num_counts = [0] * 45
    for nums in win_nums[-24:]:
        for num in nums:
            recent_num_counts[num-1] += 1
    return recent_num_counts
'''
# 최근 24회차까지의 번호 출현 횟수 구하기
def get_recent_num_counts(win_nums):
    recent_num_counts = [0] * 45
    for nums in win_nums[-24:]:
        for num in nums:
            if recent_num_counts[num-1] < 6 or recent_num_counts[num-1] > 0:
                recent_num_counts[num-1] += 1
    return recent_num_counts


# 로또 번호 예측하기
def predict_lotto_nums():
    # 이월수 구하기
    carryover_num = get_carryover_num(win_nums)

    # 역수 구하기
    reverse_num = get_reverse_num(win_nums)

    # 최근 24회차까지의 번호 출현 횟수 구하기
    recent_num_counts = get_recent_num_counts(win_nums)

    # 여기에 제외수 추가해라
    exp_nums = [1,2,8,16,39,42,44]
    
    # 번호 예측하기
    lotto_nums_set = []


    #for _ in range(20):
    while len(lotto_nums_set) < 20:
        lotto_nums = set()

        # 이월수 기반 예측
        for _ in range(random.randint(0, 2)):
            carryover_prob = [num / sum(carryover_num) for num in carryover_num]
            num = random.choices(range(1, 46), weights=carryover_prob)[0]
            lotto_nums.add(num)
            exp_nums.append(num)

        # 역수 기반 예측
        if len(lotto_nums) < 6:
            reverse_prob = [num / sum(reverse_num) for num in reverse_num]
            num = random.choices(range(1, 46), weights=reverse_prob)[0]
            if num not in lotto_nums:
                if num not in exp_nums:
                    lotto_nums.add(num)
            exp_nums.append(num)

        # 최근 24회차 기반 예측
        while len(lotto_nums) < 6:
            recent_prob = [num / sum(recent_num_counts) for num in recent_num_counts]
            num = random.choices(range(1, 46), weights=recent_prob)[0]
            if num not in lotto_nums:
                if num not in exp_nums:
                    lotto_nums.add(num)
        
        # 만든 번호가 지난 회차의 3등 이상 된적 있으면 안뽑을거임
        num_of_matching = []
        for nums in win_nums:
            num_of_matching.append(len(set(nums[:-1]) & set(lotto_nums)))
        
        if max(num_of_matching) < 4:
                lotto_nums_set.append(sorted(list(lotto_nums)))    
        
    return lotto_nums_set

# 로또 번호 예측하기
predicted_nums = predict_lotto_nums()

# 등수 리스트
rank = [".", "5등", "4등", "3등", "2등", "1등"]
lucky_number = [3,18,19,23,32,45,24]

# 결과 출력하기
print("=== 예측된 로또 번호 ===")
for nums in predicted_nums:
    match_count = len(set(nums) & set(lucky_number[:-1]))
    bonus_match = nums.count(lucky_number[-1])
    if match_count == 6:
        print(f"{nums} - {rank[5]}")
    elif match_count == 5 and bonus_match == 1:
        print(f"{nums} - {rank[4]}")
    elif match_count == 5 and bonus_match == 0:
        print(f"{nums} - {rank[3]}")
    elif match_count == 4:
        print(f"{nums} - {rank[2]}")
    elif match_count == 3:
        print(f"{nums} - {rank[1]}")
    else:
        print(f"{nums} - {rank[0]}")

#3,18,19,23,32,45,24 