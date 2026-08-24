scores = [85, 92, 78, 66, 77]

print(scores)

total_h = 0
total_l = 0

count_high = 0
count_low = 0

for score in scores:
    if score > 51:
        total_h += score
        count_high += 1
        avg_high = total_l / count_low
    
else:
    total_l += score
    count_low += 1
    avg_low = total_l / count_low


    #print(scores)
    #total=total+score


#그룹이 2그룹 상위(51~100) 하위(1~50)그룹의 합계, 인원수 평균을 각각 출력하시오.

#print(f"총 합계 점수는 {total}이고 인원은 {len(scores)}입니다.  이때 평균은 {avg}입니다.")



#total = scores[0]+scores[1]+scores[2]+ scores[3]+ scores[4]

#avg = hap / 3

#print(f"총 합계 점수는 {total}이고 이때 평균은 {avg}입니다.")

print(f"상위그룹 총 합계 점수는 {total_h}이고 인원은 {count_high}명 입니다. 이때 평균은 {avg_high}입니다")
print(f"하위그룹 총 합계 점수는 {total_l}이고 인원은 {count_low}명 입니다. 이때 평균은 {avg_low}입니다")









