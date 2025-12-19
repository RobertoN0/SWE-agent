import json
import glob
import os

def parse_swe_agent_trajectory(file_path):
    """
    Reads a SWE-agent .traj file and flattens it into a MAST-compatible text string.
    Handles potentially malformed JSON if the run was interrupted.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"⚠️ Warning: {file_path} is malformed (likely interrupted). Attempting manual fix...")
        # Simple recovery for interrupted files: read raw text and try to add closing brackets
        with open(file_path, 'r') as f:
            raw_text = f.read()
        try:
            # Attempt to close the json list/obj if it was cut off
            data = json.loads(raw_text + "]}") 
        except:
            return "ERROR: Could not parse interrupted trace file."

    # The trajectory is usually under the 'trajectory' key or is the list itself
    history = data.get('trajectory', data) if isinstance(data, dict) else data
    
    formatted_trace = []
    
    # Iterate through the steps (turns)
    for step in history:
        # 1. The Agent's Thought and Action
        if 'thought' in step and step['thought']:
            formatted_trace.append(f"Agent Thought: {step['thought']}")
        if 'action' in step and step['action']:
            formatted_trace.append(f"Agent Action: {step['action']}")
            
        # 2. The System's Observation (Output)
        if 'observation' in step and step['observation']:
            # Truncate very long outputs to save tokens (MAST doesn't need 1000 lines of ls -R)
            obs = step['observation']
            if len(obs) > 1000: 
                obs = obs[:1000] + "... [TRUNCATED]"
            formatted_trace.append(f"System Output: {obs}")
            
    return "\n\n".join(formatted_trace)

# --- EXECUTION ---
# Get all .traj files from your trajectories folder
traj_files = glob.glob("security_experiment/traces_mast_tools/SWE-agent__test-repo-i1.traj") 

for t_file in traj_files:
    flat_trace = parse_swe_agent_trajectory(t_file)
    output_filename = t_file.replace(".traj", ".txt")
    
    with open(output_filename, "w") as f:
        f.write(flat_trace)
    
    print(f"✅ Converted {t_file} -> {output_filename}")