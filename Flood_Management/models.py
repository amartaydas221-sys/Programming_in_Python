# Easha will work on

# Responsibilities
# Family class
# Add family
# View family
# Search family
# Update family
# Delete family
# Input validation
# Duplicate ID prevention
class Family:
    def __init__(self,
                 familyId,
                 headName,
                 phone,
                 district,
                 upazila,
                 village,
                 members,
                 children,
                 elderly,
                 disabledMembers,
                 damageLevel,
                 shelterNeeded,
                 receivedRelief=False):

        self.familyId = familyId
        self.headName = headName
        self.phone = phone
        self.district = district
        self.upazila = upazila
        self.village = village
        self.members = members
        self.children = children
        self.elderly = elderly
        self.disabledMembers = disabledMembers
        self.damageLevel = damageLevel
        self.shelterNeeded = shelterNeeded
        self.receivedRelief = receivedRelief

    def to_families_json(self):
        return {
            "familyId": self.familyId,
            "headName": self.headName,
            "phone": self.phone,
            "district": self.district,
            "upazila": self.upazila,
            "village": self.village,
            "members": self.members,
            "children": self.children,
            "elderly": self.elderly,
            "disabledMembers": self.disabledMembers,
            "damageLevel": self.damageLevel,
            "shelterNeeded": self.shelterNeeded,
            "receivedRelief": self.receivedRelief
        }

    def display(self):
        print("\n========== FAMILY INFORMATION ==========")
        print("Family ID         :", self.familyId)
        print("Head Name         :", self.headName)
        print("Phone             :", self.phone)
        print("District          :", self.district)
        print("Upazila           :", self.upazila)
        print("Village           :", self.village)
        print("Members           :", self.members)
        print("Children          :", self.children)
        print("Elderly           :", self.elderly)
        print("Disabled Members  :", self.disabledMembers)
        print("Damage Level      :", self.damageLevel)
        print("Shelter Needed    :", "Yes" if self.shelterNeeded else "No")
        print("Received Relief   :", "Yes" if self.receivedRelief else "No")
        print("========================================")