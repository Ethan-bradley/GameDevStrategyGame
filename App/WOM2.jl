#This part of the code defines what attributes a "Polity" will contain.  What are the modeled aspects of a country in other words.

mutable struct Polity
        Pop::Float64
        Cash::Float64
        TextCons::Float64
	GrainCons::Float64
        OilCons::Float64
	SteelCons::Float64
	TextPro::Float64
	GrainPro::Float64
	OilPro::Float64
	SteelPro::Float64
        Mills::Float64
	Fields::Float64
        Wells::Float64
	Forges::Float64
        Hours::Float64
        TextPrice::Float64
        OilPrice::Float64
	GrainPrice::Float64
	SteelPrice::Float64
	Treas::Float64
	SteelPur::Float64
end

#This part of the code defines what the price of each trade good is at any point during the calculation process in any given polity, and sets the value of the polity's price variable for that trade good equal thereto. The price is determined by the relative supply of money and the trade goods in the country.  

function computeTextPrice(Polity)
        Polity.TextPrice = Polity.Cash/(Polity.TextCons+1)
end

function computeOilPrice(Polity)
        Polity.OilPrice = Polity.Cash/(Polity.OilCons+1)
end
function computeGrainPrice(Polity)
        Polity.GrainPrice = Polity.Cash/(Polity.GrainCons+1)
end
function computeSteelPrice(Polity)
	Polity.SteelPrice = Polity.Cash*Polity.Hours/(Polity.Forges)
end

function MaxTextPrice(Polity_List,List_Length,S,Transport_Matrix)
	Price_List = [Polity_List[i].TextPrice for i in 1:List_Length] - Transport_Matrix[S]
	Max_Price = maximum(Price_List)
	Max_Price_Location = 0
	hidden = true
        while hidden
        	Max_Price_Location = Max_Price_Location + 1
                if Price_List[Max_Price_Location] == maximum(Price_List)
                	hidden = false
               	end
	end
	return(Price_List,Max_Price,Max_Price_Location)
end

function MaxGrainPrice(Polity_List,List_Length,S,Transport_Matrix)
        Price_List = [Polity_List[i].GrainPrice for i in 1:List_Length] - Transport_Matrix[S]
        Max_Price = maximum(Price_List)
        Max_Price_Location = 0
        hidden = true
        while hidden
                Max_Price_Location = Max_Price_Location + 1
                if Price_List[Max_Price_Location] == maximum(Price_List)
                        hidden = false
                end
        end
        return(Price_List,Max_Price,Max_Price_Location)
end

function MaxOilPrice(Polity_List,List_Length,S,Transport_Matrix)
        Price_List = [Polity_List[i].OilPrice for i in 1:List_Length] - Transport_Matrix[S]
        Max_Price = maximum(Price_List)
        Max_Price_Location = 0
        hidden = true
        while hidden
                Max_Price_Location = Max_Price_Location + 1
                if Price_List[Max_Price_Location] == maximum(Price_List)
                        hidden = false
                end
        end
        return(Price_List,Max_Price,Max_Price_Location)
end

function MinSteelPrice(Polity_List,List_Length,B,Transport_Matrix)
	Price_List = [Polity_List[i].SteelPrice + Transport_Matrix[i][B] for i in 1:List_Length]
        Min_Price = minimum(Price_List)
        Min_Price_Location = 0
        hidden = true
        while hidden
                Min_Price_Location = Min_Price_Location + 1
                if Price_List[Min_Price_Location] == minimum(Price_List)
                        hidden = false
                end
        end
        return(Price_List,Min_Price,Min_Price_Location)
end

#This is the function that actually conducts a trade in textiles between polities
function trade_textiles(Polity_List,List_Length,S,B,Tariff_Matrix)
	Polity_List[S].Hours = Polity_List[S].Hours + 0.01/(Polity_List[S].Mills/Polity_List[S].Pop)
	Polity_List[B].TextCons = Polity_List[B].TextCons + 0.01*Polity_List[S].Pop
	Polity_List[S].Cash = Polity_List[S].Cash + MaxTextPrice(Polity_List,List_Length,S,Tariff_Matrix)[2]*0.01*Polity_List[S].Pop-0.01*Polity_List[S].Pop*Tariff_Matrix[S][B]
	Polity_List[B].Cash = Polity_List[B].Cash - MaxTextPrice(Polity_List,List_Length,S,Tariff_Matrix)[2]*0.01*Polity_List[S].Pop
	Polity_List[S].Treas = Polity_List[S].Treas + 0.01*Polity_List[S].Pop*Tariff_Matrix[S][B]
	Polity_List[S].TextPro = Polity_List[S].TextPro + 0.01*Polity_List[S].Pop
end

#This is the function that actually conducts a trade in grain between polities
function trade_grain(Polity_List,List_Length,S,B,Tariff_Matrix)
	Polity_List[S].Hours = Polity_List[S].Hours + 0.01/(Polity_List[S].Fields/Polity_List[S].Pop)
        Polity_List[B].GrainCons = Polity_List[B].GrainCons + 0.01*Polity_List[S].Pop
        Polity_List[S].Cash = Polity_List[S].Cash + MaxGrainPrice(Polity_List,List_Length,S,Tariff_Matrix)[2]*0.01*Polity_List[S].Pop-0.01*Polity_List[S].Pop*Tariff_Matrix[S][B]
        Polity_List[B].Cash = Polity_List[B].Cash - MaxGrainPrice(Polity_List,List_Length,S,Tariff_Matrix)[2]*0.01*Polity_List[S].Pop
        Polity_List[S].Treas = Polity_List[S].Treas + 0.01*Polity_List[S].Pop*Tariff_Matrix[S][B]
	Polity_List[S].GrainPro = Polity_List[S].GrainPro + 0.01*Polity_List[S].Pop
end

#This is the function that actually conducts a trade in oil between polities
function trade_oil(Polity_List,List_Length,S,B,Tariff_Matrix)
	Polity_List[S].Hours = Polity_List[S].Hours + 0.01/(Polity_List[S].Wells/Polity_List[S].Pop)
        Polity_List[B].OilCons = Polity_List[B].OilCons + 0.01*Polity_List[S].Pop
        Polity_List[S].Cash = Polity_List[S].Cash + MaxOilPrice(Polity_List,List_Length,S,Tariff_Matrix)[2]*0.01*Polity_List[S].Pop-0.01*Polity_List[S].Pop*Tariff_Matrix[S][B]
        Polity_List[B].Cash = Polity_List[B].Cash - MaxOilPrice(Polity_List,List_Length,S,Tariff_Matrix)[2]*0.01*Polity_List[S].Pop
        Polity_List[S].Treas = Polity_List[S].Treas + 0.01*Polity_List[S].Pop*Tariff_Matrix[S][B]
	Polity_List[S].OilPro = Polity_List[S].OilPro + 0.01*Polity_List[S].Pop
end

function trade_steel(Polity_List,List_Length,S,B,Tariff_Matrix)
        Polity_List[S].Hours = Polity_List[S].Hours + 0.01/(Polity_List[S].Forges/Polity_List[S].Pop)
        Polity_List[B].SteelCons = Polity_List[B].SteelCons + 0.01*Polity_List[S].Pop
        Polity_List[S].Cash = Polity_List[S].Cash + MinSteelPrice(Polity_List,List_Length,S,Tariff_Matrix)[2]*0.01*Polity_List[S].Pop-0.01*Polity_List[S].Pop*Tariff_Matrix[S][B]
        Polity_List[B].Cash = Polity_List[B].Cash - MinSteelPrice(Polity_List,List_Length,S,Tariff_Matrix)[2]*0.01*Polity_List[S].Pop
        Polity_List[S].Treas = Polity_List[S].Treas + 0.01*Polity_List[S].Pop*Tariff_Matrix[S][B]
	Polity_List[S].SteelPro = Polity_List[S].SteelPro + 0.01*Polity_List[S].Pop
end

#This is the function that actually takes in a list of polities with all of their attributes being whatever they are and simulates economic interaction between then until market equilibirum is reached.

function run_production(Polity_List,List_Length,Transport_Matrix, Tariff_Matrix)
	#first we assume that the polities are willing to trade with each other
	trading = true
	#then we engage in certain trade-caused modifications of polity attributes as long as the trading is going on
	while trading
		#we start off each round of trading by assuming that no more trade will take place thereafter.  This will be reversed if there are any profitable trades.
		trading = false
		#we then go to each and every polity in the list to apply out trade-based changes
		for i in  1:List_Length
			l = 0
			m = 0
			n = 0
			o = 0
			
			#if the maximum textile price achievable by the polity in trade with anyone exceeds the price of labor needed to produce textiles we do several things: 
			if 10*MaxTextPrice(Polity_List,List_Length,i,Transport_Matrix)[2]*Polity_List[i].Pop > Polity_List[i].Hours*Polity_List[i].Cash/(Polity_List[i].Mills/Polity_List[i].Pop)
				l = MaxTextPrice(Polity_List,List_Length,i,Transport_Matrix)[3]
				trade_textiles(Polity_List,List_Length,i,l,Transport_Matrix)
				#Since a profitable trade occured people are still trading with each other
				trading = true
			end

			#if the maximum grain price achievable by the polity in trade with anyone exceeds the price of labor needed to produce grain we do several things:
			if 10*MaxGrainPrice(Polity_List,List_Length,i,Transport_Matrix)[2]*Polity_List[i].Pop > Polity_List[i].Hours*Polity_List[i].Cash/(Polity_List[i].Fields/Polity_List[i].Pop)
				m = MaxGrainPrice(Polity_List,List_Length,i,Transport_Matrix)[3]
				trade_grain(Polity_List,List_Length,i,m,Transport_Matrix)
				#Since a profitable trade occured people are still trading with each other
				trading = true
			end
						
			#if the maximum oil price achievable by the polity in trade with anyone exceeds the price of labor needed to produce oil we do several things:
			if 10*MaxOilPrice(Polity_List,List_Length,i,Transport_Matrix)[2]*Polity_List[i].Pop > Polity_List[i].Hours*Polity_List[i].Cash/(Polity_List[i].Wells/Polity_List[i].Pop)
				n = MaxOilPrice(Polity_List,List_Length,i,Transport_Matrix)[3]
				trade_oil(Polity_List,List_Length,i,n,Transport_Matrix)
				#Since a profitable trade occured people are still trading with each other
				trading = true
			end
			if Polity_List[i].SteelPur > Polity_List[i].SteelCons
				o = MinSteelPrice(Polity_List,List_Length,i,Transport_Matrix)[3]
				trade_steel(Polity_List,List_Length,o,i,Transport_Matrix)
				#Since a profitable trade occured people are still trading with each other
				trading = true
			end
			#Once we've made all these changes to the quantities of the different polities we need to recompute prices
			if l == 0
				l = 1
			end
			if m == 0
				m = 1
			end
			if n == 0
				n = 1
			end
			computeTextPrice(Polity_List[i])
                        computeGrainPrice(Polity_List[i])
                        computeOilPrice(Polity_List[i])
			computeSteelPrice(Polity_List[i])

			computeTextPrice(Polity_List[l])
                        computeGrainPrice(Polity_List[l])
                        computeOilPrice(Polity_List[l])
			computeSteelPrice(Polity_List[l])

			computeTextPrice(Polity_List[m])
			computeGrainPrice(Polity_List[m])
			computeOilPrice(Polity_List[m])
			computeSteelPrice(Polity_List[m])
			
			computeTextPrice(Polity_List[n])
                        computeGrainPrice(Polity_List[n])
                        computeOilPrice(Polity_List[n])
			computeSteelPrice(Polity_List[n])

			#we then print the statistics of the polity to the command line for the user to see
			print("Polity")
			print(i)
			#print("
			#TextPrice = ")
			#print(Polity_List[i].TextPrice)
			#print("
			#GrainPrice = ")
                        #print(Polity_List[i].GrainPrice)
			#print("
			#OilPrice = ")
                        #print(Polity_List[i].OilPrice)
			print("
			TextPro = ")
			print(Polity_List[i].TextPro)
			print("
			GrainPro = ")
			print(Polity_List[i].GrainPro)
			print("
			OilPro = ")
			print(Polity_List[i].OilPro)
			print("
			SteelPro = ")
			print(Polity_List[i].SteelPro)
			print("
			Hours = ")
			print(Polity_List[i].Hours)
			print("
                        Cash = ")
                        print(Polity_List[i].Cash)
			print("
                        TextCons = ")
                        print(Polity_List[i].TextCons)
                        print("
                        GrainCons = ")
                        print(Polity_List[i].GrainCons)
                        print("
                        OilCons = ")
                        print(Polity_List[i].OilCons)
			print("
			SteelCons = ")
			print(Polity_List[i].SteelCons)
			print("
			Treasury = ")
			print(Polity_List[i].Treas)
			print("

			")
		end
	end
end

# what is above are the functions that we will use in the running of our example code.  These functions will need to be called in the program below.  They will not run based on the code above.

#Tell the user to enter the number of polities they want to simulate
print("Enter Number of Polities")

#The computer then stores their input in a variable.  If they didn't enter a number it won't wort
x = readline()

#Generate a list of polities of the length the user specified
Polity_List = [Polity(100,100,0,0,0,0,0,0,0,0,100,100,100,100,0,0,0,0,0,0,0) for i in 1:parse(Int64,x)]

#this code generates some test polities that are not identical to simulate some trade.
Polity_List[1] = Polity(100,100,0,0,0,0,0,0,0,0,100,100,100,100,0,0,0,0,0,0,20)

Polity_List[2] = Polity(100,100,0,0,0,0,0,0,0,0,100,100,500,100,0,0,0,0,0,0,0)

#this code creates a 2 dimensional matrix with the same length as the polity list.  This will have enough space to store one value for each polity's tariff on each other in the indecies of the polities.
Transport_Matrix = [[parse(Float64,"0") for i in 1:parse(Int64,x)] for i in 1:parse(Int64,x)]
Transport_Matrix[1][2] = 100
Transport_Matrix[2][1] = 100
Tariff_Matrix = [[parse(Float64,"0") for i in 1:parse(Int64,x)] for i in 1:parse(Int64,x)]

#start by computing prices in all the polities based on their starting charectaristics
for i in 1:parse(Int64,x)
	computeTextPrice(Polity_List[i])
	computeGrainPrice(Polity_List[i])
	computeOilPrice(Polity_List[i])
end

#Ask the user for tariffs to fill each spot on the tariff matrix.  Yes I made a tariff and transport matrix and then stored the tariff values alone in the transport matrix.  I'll fix it later.
for i in 1:parse(Int64,x)
        for j in 1:parse(Int64,x)
                print("
                What tariff does polity")
                print(i)
                print("put on exports to polity")
                print(j)
		print("
		")
		Transport_Matrix[i][j] = parse(Float64,readline())
	end
end

#run the economic interaction function on the list of polities generated and the matrix of tariffs entered.  That function has print commands so there's no need to print anything manually here.
run_production(Polity_List,parse(Int64,x),Transport_Matrix,Transport_Matrix)

#Ask the user for an exit command to keep the program open as long as the user wants to look at the polity attributes printed by the run_production function
print("Enter Exit Command")

e = readline()
