# 🔒 Renewing SSL Certificate for radionova.no
We are working on an automatic SSL certificate provider/tool for radionova.no but for now:
This guide shows how to renew or create a new **App Service Managed Certificate** for `radionova.no`.  
It takes about **10 minutes** and requires no coding.

---

## Step 1 — Check your domain status
Go to your **App Service → Custom domains** in the Azure portal.

You’ll see your domain and its certificate status.  
If it says **Certificate expired**, it means the HTTPS certificate needs renewal.

![Custom domain view showing expired certificate](https://github.com/user-attachments/assets/451790ce-bf26-4ac8-b84a-9b81c1ac4015)

 Tip: Make sure your DNS A-record in Domeneshop points to **20.79.107.2** (the Azure App Service IP).

---

## Step 2 — Open the certificate section
From the left menu, go to  
**TLS/SSL Settings → Private Key Certificates (.pfx)** → **Managed certificates** tab.

You’ll see the expired certificate listed.  
We’ll delete and recreate it.

![Expired managed certificate view](https://github.com/user-attachments/assets/dc37e060-175a-4c6d-ac3c-62a90fe24399)

---

## Step 3 — Delete the expired certificate
Click on the expired certificate → **Delete**.  
This removes the old one but keeps your domain intact.

Now we’ll add a fresh certificate.

---

## Step 4 — Create a new managed certificate
Click **+ Add certificate → Create App Service Managed Certificate**.  
Choose your custom domain (`radionova.no`) and give it a friendly name (for example `radionova.no-radionova`).

Click **Add** to start generation.  
Azure will create a **free, trusted SSL certificate** that auto-renews every 6 months.

![Creating new managed certificate](https://github.com/user-attachments/assets/855840e0-b41f-4793-beb6-2f9346dc7d9e)

> ⏳ It takes about 5–10 minutes. You’ll get a notification once it’s ready.

---

## Step 5 — Bind the new certificate
After it’s issued, go back to  
**Custom domains → Update binding.**

Select:
- **Certificate:** your new one (`radionova.no-radionova`)  
- **TLS/SSL type:** SNI SSL  

Then click **Update**.

![Binding the new SSL certificate](https://github.com/user-attachments/assets/ffd9fc5e-d77e-4d28-8571-70cf70e0357b)

> This links your new certificate to your domain.  
> HTTPS will now be active and valid again.

---

## Step 6 — Verify
Visit [https://radionova.no](https://radionova.no) —  
You should now see the padlock 🔒 and **“Connection is secure.”**

---

## Notes
- The certificate renews **automatically** before expiry.  
- Managed certificates are **free** with Azure App Service.  
- If auto-renew ever fails, repeat this same process.

---


**Last updated:** October 2025
