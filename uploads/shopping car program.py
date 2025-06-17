#shopping cart program

foods = []
prices = []
total = 0

while True:
  food = input("enter the food you want to buy (enter q to quit): ")
  if food.lower() == 'q': #lower is used just incase if the user types caps Q
    break
  else:
    price = int(input(f"enter the price of the {food}: $"))
    foods.append(food)
    prices.append(price)
print("--------YOUR CART-----------")

for food in foods:
  print(foods, end = " ")
for price in prices:
  total += price
print()
print(f"YOUR TOTAL IS ${total}")