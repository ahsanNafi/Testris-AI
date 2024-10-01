import unittest
import trainer
import random

seed = 1
test_modifier1 = [1/4, 1/4, 1/4, 1/4]
test_modifier2 = [1/5, 2/5, 1/5, 1/5]
test_epoch =  [
    [0.25,                  0.16666666666666666,    0.4166666666666667,     0.16666666666666666],
    [0.25806451612903225,   0.25806451612903225,    0.25806451612903225,    0.22580645161290322],
    [0.26666666666666666,   0.13333333333333333,    0.5333333333333333,     0.06666666666666667],
    [0.30434782608695654,   0.30434782608695654,    0.043478260869565216,   0.34782608695652173],
    [0.29411764705882354,   0.23529411764705882,    0.11764705882352941,    0.35294117647058826]]
new_test_epoch = [
    [0.25,                  0.16666666666666666,    0.4166666666666667,     0.16666666666666666], 
    [0.27340978028059054,   0.19740999982149224,    0.2822294506122225,     0.24695076928569468], 
    [0.19903195055797962,   0.24566432187359089,    0.39664551969173534,    0.1586582078766941], 
    [0.26666666666666666,   0.13333333333333333,    0.5333333333333333,     0.06666666666666667], 
    [0.3161442402980535,    0.15807212014902675,    0.051545256570334805,   0.474238382982585]]
test_fitness = [1, 1, 4, 5, 5]


class Test_trainer(unittest.TestCase):
    
    def setUp(self):
        self.trainer = trainer.Trainer()
        self.trainer.set_seed(seed)
        self.trainer.size = 5
    
    def tearDown(self):
        self.trainer.population = None
        self.trainer.fitness = []
        pass
    
    def test_seed(self):
        self.assertEqual(self.trainer.get_seed(), seed)
    def test_seed_gen(self):
        self.assertEqual(self.trainer.gen_seed(), 3201)
        
    def test_normalize(self):
        self.assertEqual(self.trainer.normalize([1,1,1,1]), [0.25,0.25,0.25,0.25])
    def test_norm_sum(self):
        rand_mod = [random.random() for x in range(4) ]
        self.assertAlmostEqual(sum(self.trainer.normalize(rand_mod)), 1)
    
    def test_gen_new_epoch(self):
        self.assertEqual(self.trainer.gen_epoch(seed), None)
        self.assertEqual(self.trainer.population,test_epoch)
        
        self.trainer.fitness = test_fitness
        self.trainer.gen_epoch(seed)
        print(f"\n{self.trainer.population}\n")
        self.assertEqual(self.trainer.population, new_test_epoch)
        
    def test_cross_breed(self):
        breed = ([0.2735706338007598, 0.28871635211802466, 0.21885650704060786, 0.21885650704060786], 
                 [0.14368394059927286, 0.38058491528921207, 0.23786557205575753, 0.23786557205575753])
        self.assertEqual(self.trainer.cross_breed(test_modifier1,test_modifier2), breed)
        
    def test_mod_gen(self):
        self.assertEqual(self.trainer.gen_mod_rand(),[0.25, 0.16666666666666666, 0.4166666666666667, 0.16666666666666666])
        
    def test_mutate(self):
        self.assertEqual(self.trainer.mutate(test_modifier1), [0.25, 0.26384077496444247, 0.25, 0.25])
    
    def test_fitness(self):
        pass # function not created
        
if __name__ == '__main__':
    unittest.main()