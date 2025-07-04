
![PlanningSystem](Docs/images/planning_system.png)

# zh_CN [简体中文](README.md)
# [Project Document](Docs/OpenAPS.pdf)

# What's APS
APS (Advanced Planning and Scheduling) is a system used to optimize and manage complex operational processes in manufacturing, logistics, and other industries. It aims to generate efficient, feasible plans and schedules by considering multiple factors and constraints, thereby improving operational efficiency and resource utilization.

# OpenAPS

## Project Objective

<ol>
    <li>Promote the widespread adoption of APS</li>
    <li>Provide efficient tools to help enterprises make scientific decisions in production scenarios</li>
    <li>Break the complexity of traditional APS system implementation—ready to use after data configuration</li>
    <li>Combine specialized mathematical models and constraint solving for reliable optimization</li> <li>Explore best practices of APS</li>
    <li>Provide reference and learning resources</li>
</ol>

## Project Features
Represent actual planning/decision problems through constraint optimization mathematical models.

## Project Objectives
The current APS (Advanced Planning and Scheduling) systems face several critical challenges and needs:

### 1. Lack of Targeted Mathematical Models and Suitable Algorithms
Despite the abundance of systems, they often lack mathematical models and algorithms that accurately reflect real business needs. This results in suboptimal performance and prevents APS systems from realizing their full potential. By developing mathematical models and optimization algorithms that align with real business needs, the project aims to enhance the targeting and practicality of APS systems, ensuring they can effectively solve real problems.

### 2. High Implementation Complexity
Implementing APS systems often involves complex project cycles with uncertain outcomes. Through modular design and standardized processes, the project aims to reduce the complexity of implementing APS systems, shorten project cycles, and improve the certainty of project outcomes.

### 3. Overemphasis on Process Coordination, Lacking Optimization and Collaboration Integration
Current APS systems frequently focus too much on process coordination while neglecting the organic integration of optimization algorithms with collaboration. This leads to suboptimal coordination and fails to maximize overall benefits.

### 4. High Customization Leading to Difficulty in Adapting to Change
During implementation, APS systems are prone to becoming highly customized information systems, making them difficult to adapt to changing business environments and even leading to failure due to incompatibility.

### 5. Insufficient Human-Computer Interaction
The optimization process lacks sufficient human-computer interaction, causing discrepancies between the optimization logic and actual business needs, which affects the effectiveness of optimization decisions.

## Overall Solution
Global Collaboration and Decision Optimization

![计划体系的协同方案](Docs/images/collaboration_approach.png)

## Application Scenarios:
<ol>
    <li>Planning</li>
    <ol>
        <li>Master Production Scheduling</li>
        <li>Job Scheduling/Production Scheduling</li>
        <li>Capacity Planning</li>
        <li>Material Requirement Planning</li>
    </ol>
    <li>Multi-Plan Coordination</li>
    <ol>
        <li>Coordination between Master Production Scheduling and Job Scheduling</li>
        <li>Coordination between Master Production Scheduling and Procurement Planning</li>
        <li>Coordination between Master Production Scheduling and Capacity Planning</li>
    </ol>
    <li>Supply Chain Coordination</li>
</ol>

## Getting started

### When you first clone the repository you'll need to update the submodules:

    ```
    git submodule update --init --recursive
    ```

### Then update all submodules

    ```
    git submodule update --recursive --remote
    ```

### Install Packages Using requirements.txt

    ```
    pip install -r requirements.txt
    ```

## Project Structure
|   | Submodule                  | Description                                             |
|:--|:---------------------------|:--------------------------------------------------------|
| 1 | Application                | Various scenarios and applications.                     |
| 2 | DataSets                   | Public data sets.                                       |
| 3 | Interface                  | Data interfaces.                                        |
| 4 | OptimizationCalculusKernel | mathematical models and algorithms needed for planning. |

### Demos

    ```
    python3 Applications/ProductionPlanning/Workshop.py
    python3 Applications/ProductionScheduling/CircularSequence.py
    python3 Applications/Demos/main.py
    ```

## about GOCK

GOCK is a Mathematical Programming and Constraint Solving Tools for Industrial software

![gock](Docs/images/gock.png)
