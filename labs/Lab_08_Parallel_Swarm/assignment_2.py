from concurrent.futures import ThreadPoolExecutor

def research_agent(goal):
    return {"role":"research","output":"Past events favored a 24-hour themed hackathon."}
def logistics_agent(goal):
    return {"role":"logistics","output":{"venue":"Grand Hall","venue_cost":45000,"date":"Saturday","capacity":100}}
def budget_agent(goal):
    return {"role":"budget","output":{"total_cap":30000}}
def judging_agent(goal):
    return {"role":"judging","output":{"criteria":"Innovation, technical depth, and demo quality","judges_available":3}}
def marketing_agent(goal):
    return {"role":"marketing","output":{"publicity_plan":"Social media campaign","marketing_cost":8000}}

ROLES={"research":research_agent,"logistics":logistics_agent,"budget":budget_agent,"judging":judging_agent,"marketing":marketing_agent}
def run_swarm(goal):
    with ThreadPoolExecutor(max_workers=len(ROLES)) as pool:
        futures={name:pool.submit(fn,goal) for name,fn in ROLES.items()}
        return {name:future.result() for name,future in futures.items()}

def merge(o):
    return {"format_notes":o["research"]["output"],"venue":o["logistics"]["output"]["venue"],"venue_cost":o["logistics"]["output"]["venue_cost"],"date":o["logistics"]["output"]["date"],"venue_capacity":o["logistics"]["output"]["capacity"],"budget_cap":o["budget"]["output"]["total_cap"],"judging_criteria":o["judging"]["output"]["criteria"],"judges_available":o["judging"]["output"]["judges_available"],"publicity_plan":o["marketing"]["output"]["publicity_plan"],"marketing_cost":o["marketing"]["output"]["marketing_cost"]}

def research_critique(d):
    return [] if "24-hour" in d["format_notes"] else [{"role":"research","objection":"The plan does not preserve the researched 24-hour format."}]
def logistics_critique(d):
    return [{"role":"logistics","objection":f"Venue capacity {d['venue_capacity']} may be too small for 150 participants."}] if d["venue_capacity"]<150 else []
def budget_critique(d):
    total=d["venue_cost"]+d["marketing_cost"]
    return [{"role":"budget","objection":f"Combined cost {total} exceeds budget cap {d['budget_cap']}."}] if total>d["budget_cap"] else []
def judging_critique(d):
    return [{"role":"judging","objection":f"Only {d['judges_available']} judges available; four are preferred."}] if d["judges_available"]<4 else []
def marketing_critique(d):
    return [{"role":"marketing","objection":f"Marketing cost {d['marketing_cost']} exceeds role target allocation 5000."}] if d["marketing_cost"]>5000 else []

CRITIQUERS={"research":research_critique,"logistics":logistics_critique,"budget":budget_critique,"judging":judging_critique,"marketing":marketing_critique}
def distributed_critique(d):
    with ThreadPoolExecutor(max_workers=len(CRITIQUERS)) as pool:
        futures={role:pool.submit(fn,d) for role,fn in CRITIQUERS.items()}
        return [item for role,future in futures.items() for item in future.result()]

if __name__=="__main__":
    outputs=run_swarm("Plan a college AI hackathon")
    draft=merge(outputs)
    print("=== Merged draft ===")
    print(draft)
    print("\\n=== Distributed critique ===")
    log=distributed_critique(draft)
    for entry in log: print(entry)
    roles={entry["role"] for entry in log}
    print("\\nRoles raising objections:",sorted(roles))
    print("Independent objections:",len(log))
    assert len(roles)>=2
    print("Check passed: at least two distinct roles independently raised objections.")
