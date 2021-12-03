import pytest
from simulation import Simulation
from logger import Logger
from person import Person
from virus import Virus

def test_virus_instantiation():
  virus=Virus("skin", .3, 2)
  assert virus.name == "skin"
  assert virus.repro_rate == .3
  assert virus.mortality_rate == 2

def test_simulation_instantiation():
  sim = Simulation(20, .2, 1, "tonsils")
  assert sim.virus_name == "tonsils"
  assert sim.pop_size == 20
  assert sim.initial_infected == 1

def test_create_population():
  sim = Simulation(10, .5, 1, "test")
  sim._create_population
  assert sim.pop_size == 10
  assert sim.population[0].infection == True
  assert sim.population[1].infection == False




# ------- RUN TESTS ------------ #
if __name__ == "__main__":
  test_virus_instantiation()
  test_simulation_instantiation()
  test_create_population()









