import pytest
from simulation import Simulation
from logger import Logger
from person import Person
from virus import Virus


virus = None
sim = None

def test_virus_instantiation():
  virus=Virus("skin", .3, 2)
  assert virus.name == "skin"
  assert virus.repro_rate == .3
  assert virus.mortality_rate == 2

def test_simulation_instantiation():
  sim = Simulation(20, .2, virus, 1)
  assert sim.pop_size == 20
  assert sim.initial_infected == 1

def test_create_population():
  sim.population = sim._create_population
  assert sim.pop_size == 10

def test_time_step():
  sim.time_step()

def test_log_infect_surv():
  sim.logger.log_infection_survival(sim.get_random_person(), True)

def test_get_random_person():
  print(sim.get_random_person())

# ------- RUN TESTS ------------ #
if __name__ == "__main__":
  # test_virus_instantiation()
  # test_simulation_instantiation()
  # test_create_population()
  # test_time_step()
  # test_log_infect_surv()
  # test_get_random_person()






