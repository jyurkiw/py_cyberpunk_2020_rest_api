from flask import Flask
from flask_restful import Resource, Api
from flask_debug import Debug
from flask_cors import CORS

from equipment import *
from stats import *
from skills import *
from lifepath import *
from cybernetics import *
from characters import *

app = Flask(__name__)
api = Api(app)
Debug(app)
CORS(app)

# Add sub-api routes
# Weapons
api.add_resource(WeaponsListApi, "/weapons/list/")
api.add_resource(WeaponCategoriesListApi, "/weapons/categories/list/")
api.add_resource(
    WeaponsByAvailabilityApi, "/weapons/availability/<string:availability>/"
)
api.add_resource(WeaponsByCategoryApi, "/weapons/category/<string:category>/")
api.add_resource(
    WeaponsByConcealabilityApi,
    "/weapons/concealability/<string:concealability>/",
)
api.add_resource(WeaponsByFilterApi, "/weapons/filter/")

# Armor
api.add_resource(ArmorListApi, "/armor/list/")
api.add_resource(ArmorHelmetApi, "/armor/helmets/")
api.add_resource(ArmorJacketApi, "/armor/jackets/")
api.add_resource(ArmorPantsApi, "/armor/pants/")
api.add_resource(ArmorByFilterApi, "/armor/filter/")

# Stat Blocks
api.add_resource(StatBlockApi, "/stats/random/<int:points>")
api.add_resource(StatBlockFinalizeApi, "/stats/finalize/")

# Career skills
api.add_resource(CareersListApi, "/careers/list/")
api.add_resource(SkillsListApi, "/skills/list/")
api.add_resource(
    CareerSkillsForRoleApi, "/skills/list/career/<string:role_name>/",
)
api.add_resource(
    CareerRandomSkillsByRoleApi,
    "/skills/random/career/<string:role_name>/points/<int:points>/",
)
api.add_resource(
    CareerRandomSkillsAndRoleApi, "/skills/random/career/points/<int:points>/",
)
api.add_resource(
    SkillsAndRoleRandomCompleteApi,
    "/skills/role/random/complete/points/<int:career_skill_points>/<int:pickup_skill_points>/",
)
api.add_resource(PickupRandomSkillsApi, "/pickupskills/random/add/")

# Lifepath
api.add_resource(LifepathRandomOriginsApi, "/lifepath/random/origins/")
api.add_resource(LifepathRandomFamilyApi, "/lifepath/random/family/")
api.add_resource(LifepathRandomMotivationsApi, "/lifepath/random/motivations/")
api.add_resource(LifepathRandomLifeEventsApi, "/lifepath/random/life_events/")
api.add_resource(LifepathRandomCompleteApi, "/lifepath/random/complete/")
api.add_resource(
    LifepathRandomStyleAndMotivationsApi, "/lifepath/random/style/motivations/"
)
api.add_resource(
    LifepathRandomFamilyAndEventsApi, "/lifepath/random/family/events/"
)

# Cybernetics
api.add_resource(
    CyberneticsClassificationsListApi, "/cyber/classification/list/"
)
api.add_resource(
    CyberneticsListByClassificationApi,
    "/cyber/classification/<string:classification>/",
)
api.add_resource(
    CyberneticsListByRequirementApi, "/cyber/requirement/<string:requirement>/",
)
api.add_resource(
    CyberneticsGetRandomApi, "/cyber/random/",
)

# Characters
api.add_resource(CharactersRandomSingleApi, "/characters/random/single/")

if __name__ == "__main__":
    app.run(debug=True)
