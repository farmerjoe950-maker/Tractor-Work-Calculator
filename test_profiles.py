from modules.profile_manager import(
    add_tractor_profile,
    delete_tractor_profile,
    load_tractors,
    load_implements
    
)

#print("=== 1. Loading Profiles ===")
#profiles = load_profiles_tractor()
#for name, specs in profiles.items():
 #   print(
  #      f"- {name}: Fuel Burn = {specs["fuel_burn_hour"]} gal/hr, Wear="
   #     f" ${specs['wear_cost']}/hr"
    #)

#print("\n=== 2. Added a New Custom Tractor ===")
#add_tractor_profile(
 #   name="Mahindra 4540",
  #  fuel_burn_hour=2.1,
   # wear_cost=3.75
#)

#print("\n=== 3. Updated Profile List ===")
#updated_profiles = load_profiles_tractor()
#for name in updated_profiles:
 #   print(f"- {name}")

tractors = load_tractors()
for name in tractors.items(): 
    print(
        f" {name}"
    )

#add_tractor_profile(name= "Mahindra 4540",
    #HP= 45,
    #fuel_burn_hour= 2.1,
    #wear_cost= 3.75
#)

implements = load_implements()
for name in implements.items():
    print(
        f" {name}"
    )