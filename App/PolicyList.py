from .models import Policy, PolicyGroup, Player
from .forms import PolicyCreateForm

class PolicyList():
	def __init__(self):
		policyOne = ['Pension Plan', ['Government Funded Plan', {'WelfareEffect':0.2, 'InequalityEffect':-0.2}], ['Mandatory Personal Savings Plan', {'SavingsEffect': 0.2, 'InequalityEffect':-0.1}], ['Optional Personal Savings Plan',{'SavingsEffect':0.05}],['No Pension Plan', {}]]
		policyTwo = ['Unemployment Welfare', ['Large Plan', {'WelfareEffect':0.15}], ['Medium Plan', {'WelfareEffect':0.1}],['Small Plan', {'WelfareEffect':0.05}], ['Mandatory Savings Plan', {'SavingsEffect':0.1}]]
		#policyThree = ['Financial Regulation', ['High',{''}]]
		policyThree = ['Unions', ['Unions Banned', {'WageEffect':-0.1}], ['Unions Allowed but power limited', {}], ['Unions Encouraged', {'WageEffect':0.1}], ['Unions Mandatory', {'WageEffect':0.2}]]
		policyFour = ['Minimum Wage', ['None',{}], ['Low',{'WageEffect':0.05}],['Medium',{'WageEffect':0.1}],['High',{'WageEffect':0.15}]]
		policyFive = ['Child Subsidies', ['Subsidies for fewer children',{'WelfareEffect':0.02, 'PopEffect':-0.005}],['None',{}],['Small Subsidies',{'WelfareEffect':0.02,'PopEffect':0.005}],['Medium Subsidies',{'WelfareEffect':0.05, 'PopEffect':0.01}],['Large Subsidies', {'WelfareEffect':0.1, 'PopEffect':0.015}]]
		self.policyList = [policyOne, policyTwo, policyThree, policyFour, policyFive]

	def add_policies(self, p, g, request=None):
		for i in self.policyList:
			group_name = i[0]
			p_group = PolicyGroup(game=g, player=p, name=group_name)
			p_group.save()
			for j in range(1,len(i)): 
				name = i[j][0]
				diction = i[j][1]
				p2 = Policy(policy_group=p_group, game=g, player=p, name=name, applied=False, SavingsEffect=0, ConsumptionEffect=0, WelfareEffect=0, InequalityEffect=0, HealthSpend=0, Healthcare=0, ConsumerLoans=0, Education=0, GovGoods=0, WageEffect=0, PopEffect=0)
				p2.save()
				print(p2.id)
				for k in diction:
					print("k: "+k)
					print("value: "+str(diction[k]))
					val = setattr(p2, k, diction[k])
					#print("val "+str(val))
					#val = diction[k]
				p2.save()
