# Create an EC2 Instance

### Task 1. Create an EC2 Instance

1. Choose the **Services** menu, locate the **Compute** services, and select **EC2**.

2. Choose the **Launch instance** button in the middle of the page, and then select **Launch instance** from the dropdown menu.

3. Name the instance:

   - Give it the name `Web Server 1` 

4. Choose an AMI from which to create the instance:

   - In the list of available *Quick Start* AMIs, keep the default **Amazon Linux** AMI selected. 

   - Also keep the default **Amazon Linux 2023 AMI x86_64 (HVM)** selected.

5. Specify an Instance type:

   - In the *Instance type* panel, keep the default **t2.micro** selected.

6. Select the key pair to associate with the instance:

   - From the **Key pair name** menu, select **vockey**.

7. Next to Network settings, choose **Edit**.

8. Keep the default *VPC* and *subnet* settings. Also keep the **Auto-assign public IP** setting set to **Enable**.

9. Under *Firewall (security groups)*, keep the default  **Create security group** option chosen.

10. Configure a new security group:

    - Keep the default selection **Create a new security group**.
    - **Security group name:** Clear the text and enter `Web Server` 
    - **Description:** Clear the text and enter `Security group for my web serverAt the bottom of the **Summary** panel on the right side of the screen choose **Launch instance**
    - You will see a Success message.

11. Choose **View all instances**

    - The instance will first appear in the *Pending* state, which means it is being launched. The state will then change to *Running*, which indicates that the instance has started booting. It takes a few minutes for the instance to boot.
    - Select the **Web Server 1** instance, and review the information in the **Details** tab that displays in the lower pane.
    - Notice that the instance has a **Public IPv4 address**. You can use this IP address to communicate with the instance from the internet.
    - Copy and save this **Public IPv4 address** in your notes

12. Before you continue, wait for your instance to display the following:

- **Instance state:** *Running*
- **Status check:** *2/2 checks passed*
-  This may take a few minutes. Choose the refresh  icon at the top of the page every 30 seconds or so to more quickly become aware of the latest status of the instance. 

## Task 2. Update the security group

1. Return to the **EC2 Management Console** browser tab. 

2. In the left navigation pane, under **Network & Security**, choose **Security Groups**. 

3. Select the **Web Server** security group, which you created when launching your EC2 instance. 

4. In the lower pane, choose the **Inbound rules** tab. 

5. Choose **Edit inbound rules**, and then choose **Add rule**. Configure the following:

   - **Type:** Custom TCP

   - **Port Range**: 8000

   - **Source:** Anywhere-IPv4
   
   - Choose **Save rules**

The new inbound HTTP rule creates an entry for IPv4 IP (0.0.0.0/0) and IPv6 IP addresses (::/0).

## Task 3. Download your key

1. Return to the lab session within AWS Academy

2. Click **AWS Details** in the menu at the top

3. Click "**Download PEM**" next to SSH Key (For Windows, download the PPK file and load into Putty)

4. On your Mac, open a terminal and type the following (If you are using Windows, talk to the TA)

   ```
   mv ~/Downloads/labsuser.pem ~/
   chmod 600 ~/labsuser.pem
   xattr -c ~/labsuser.pem
   ```

