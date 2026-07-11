wallbeers=99
while wallbeers >=0:
	if wallbeers>2:
		print(f"{wallbeers} bottles of beer on the wall, {wallbeers} bottles of beer.\nTake one down and pass it around, {wallbeers-1} bottles of beer on the wall.\n")
	elif wallbeers==2:
		print(f"{wallbeers} bottles of beer on the wall, {wallbeers} bottles of beer. \nTake one down and pass it around, {wallbeers-1} bottle of beer on the wall.\n")
	elif wallbeers==1:
		print(f"{wallbeers} bottle of beer on the wall, {wallbeers} bottle of beer. \nTake one down and pass it around, no more bottles of beer on the wall.\n")
	else: print("No more bottles of beer on the wall, no more bottles of beer. \nGo to the store and buy some more, 99 bottles of beer on the wall.")
	wallbeers-=1
