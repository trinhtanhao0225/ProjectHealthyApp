from datetime import datetime
import pandas as pd
import numpy as np
import ast  # thay eval an toàn hơn

from backend.core import database as db
from backend.models.exercise_group import ExerciseGroup
from backend.models.exercise_detail import ExerciseDetail
from backend.models.workout_plan import WorkoutPlan
from bson import ObjectId  # import nếu cần dùng trực tiếp

class ExerciseService:
    def __init__(self):
        # load dataset
        self.df = pd.read_csv("C:\\Code\\Project_healthyApp\\data\\processed\\processed_data_filtered.csv")

    # -------------------------
    # GROUP
    # -------------------------
    async def addExerciseGroup(self, email, group_name):
        group = ExerciseGroup(
            email=email,
            group_name=group_name
        )
        await group.insert()
        return {"group_name": group_name}

    async def getGroup(self, group_name):
        group = await ExerciseGroup.find_one(ExerciseGroup.group_name == group_name)
        if not group:
            return None
        doc = group.dict()  # hoặc group.model_dump() nếu Pydantic v2
        if '_id' in doc:
            doc['id'] = str(doc.pop('_id'))
        return doc

    async def getGroupsByEmail(self, email):
        groups = await ExerciseGroup.find(ExerciseGroup.email == email).to_list()
        return [
            {**g.dict(), "id": str(g.id)} if hasattr(g, 'id') else {**g.dict(), "id": str(g._id)}
            for g in groups
        ]  # dùng g.id nếu Beanie expose, fallback _id

    # -------------------------
    # EXERCISE DETAIL
    # -------------------------
    async def addExerciseDetail(self, email, group_name, exercise_name, sets, reps):
        detail = ExerciseDetail(
            email=email,
            group_name=group_name,
            name=exercise_name,
            sets=sets,
            reps=reps
        )
        await detail.insert()
        return {"exercise": exercise_name}

    async def getExerciseDetail(self, id: str):
        detail = await ExerciseDetail.get(ObjectId(id))
        if not detail:
            return None
        doc = detail.dict()
        if '_id' in doc:
            doc['id'] = str(doc.pop('_id'))
        return doc

    async def getExercisesByEmailAndGroup(self, email: str, group_name: str):
        details = await ExerciseDetail.find(
            ExerciseDetail.email == email,
            ExerciseDetail.group_name == group_name
        ).to_list()
        
        return [
            {**d.dict(), "id": str(d.id)} if hasattr(d, 'id') else {**d.dict(), "id": str(d._id)}
            for d in details
        ]

    # -------------------------
    # PLAN
    # -------------------------
    async def addExercisePlan(self, data):
        plan = WorkoutPlan(
            email=data.email,
            group_name=data.group_name,
            day=data.day,
            session=data.session,
            done_flag=False
        )
        await plan.insert()
        return {"plan": f"{data.group_name}-{data.day}-{data.session}"}

    async def getPlansByEmail(self, email: str):
        plans = await WorkoutPlan.find(WorkoutPlan.email == email).to_list()
        return [
            {**p.dict(), "id": str(p.id)} if hasattr(p, 'id') else {**p.dict(), "id": str(p._id)}
            for p in plans
        ]

    async def getPlansByEmailAndDay(self, email: str, day: str):
        plans = await WorkoutPlan.find(
            WorkoutPlan.email == email,
            WorkoutPlan.day == day
        ).to_list()
        return [
            {**p.dict(), "id": str(p.id)} if hasattr(p, 'id') else {**p.dict(), "id": str(p._id)}
            for p in plans
        ]

    async def updateDoneFlag(self, email, group_name, day, session):
        plan = await WorkoutPlan.find_one(
            WorkoutPlan.email == email,
            WorkoutPlan.group_name == group_name,
            WorkoutPlan.day == day,
            WorkoutPlan.session == session
        )
        if plan:
            plan.done_flag = True
            await plan.save()
            return {"status": "updated", "message": "Done flag set to True"}
        return {"status": "not_found", "message": "Plan not found"}

    # -------------------------
    # DATASET (giữ nguyên, chỉ thêm type hint nhỏ)
    # -------------------------
    def filterExercises(self, category: str = None, equipment: str = None, muscle: str = None):
        print("!!! DEBUG: filterExercises called with:", category, equipment, muscle)
        df = self.df.copy()

        if category:
            df = df[df["category"] == category]

        if equipment:
            df = df[df["equipment"].str.contains(equipment, case=False, na=False)]

        if muscle:
            df = df[df["combined_muscles"].str.contains(muscle, case=False, na=False)]

        df = df.replace([np.inf, -np.inf, np.nan], None).fillna(None)
        print("!!! After filter & clean - rows:", len(df))
        return df.head(50).to_dict(orient="records")

    def getExerciseInfoByName(self, name: str):
        row = self.df[self.df["name"] == name]
        if row.empty:
            return None
        return row.iloc[0].to_dict()

    def estimateCaloriesByName(self, name: str, weight: float, duration: int):
        row = self.df[self.df["name"] == name]
        if row.empty:
            return None
        met = row.iloc[0].get("MET", 0)
        calories = met * weight * (duration / 60) * 1.05  # điều chỉnh công thức nếu cần chính xác hơn
        return {"exercise": name, "calories": round(calories, 2)}

    def getMuscles(self):
        muscles = set()
        for m in self.df["combined_muscles"]:
            try:
                arr = ast.literal_eval(m)
                muscles.update(arr)
            except:
                pass
        return sorted(list(muscles))

    def getEquipment(self):
        equipment = set()
        for e in self.df["equipment"]:
            try:
                arr = ast.literal_eval(e)
                equipment.update(arr)
            except:
                pass
        return sorted(list(equipment))

    def getDependentFilters(self, muscle: str):
        df = self.df[self.df["combined_muscles"].str.contains(muscle, case=False, na=False)]
        equipment = set()
        for e in df["equipment"]:
            try:
                arr = ast.literal_eval(e)
                equipment.update(arr)
            except:
                pass
        return sorted(list(equipment))