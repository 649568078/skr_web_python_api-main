import random

# 生成一个随机数
random_number = random.randint(1, 100)

# 判断随机数属于哪个区间
interval = (random_number - 1) // 10

if interval == 9:
    print(f"随机数 {random_number} 属于区间 91 到 100")
else:
    start = interval * 10 + 1
    end = start + 9
    print(f"随机数 {random_number} 属于区间 {start} 到 {end}")