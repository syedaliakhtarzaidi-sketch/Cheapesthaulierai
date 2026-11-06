
import streamlit as st
import urllib.parse

st.set_page_config(page_title="Sahara UK Foods - Cheapest Haulier AI", layout="wide")

st.markdown("<h1 style='color:#E65100'>🧡 Sahara UK Foods — Cheapest Haulier AI</h1><p>Logistics Manager - Ali | 3 Ports • 14 Warehouses • Emails + Outlook Draft</p>", unsafe_allow_html=True)

WAREHOUSES = {
    "PE2 7LB - JSD warehouse": "JSD Warehouse, Peterborough, PE2 7LB, UK",
    "PE20 3NE - Mason Brother": "Mason Brothers, North End, Boston Road, Swineshead, Boston, Lincolnshire, PE20 3NE, UK",
    "TF3 3AY - Simmonds Warehouse": "Simmonds Transport Ltd / International House, Stafford Park 11, Telford, Shropshire, TF3 3AY, UK",
    "LL13 9UY - Proserve warehouse": "Proserve Warehouse, Wrexham, LL13 9UY, UK",
    "WA8 8RB - SSO Widnes": "SSO Widnes, Widnes, WA8 8RB, UK",
    "WA11 9SR - SSO Haydock": "SSO Haydock, Haydock, WA11 9SR, UK",
    "WA9 3NA - SSO ST Helen": "SSO St Helens, St Helens, WA9 3NA, UK",
    "WV10 9QD - AIB Foods": "AIB Foods, Wolverhampton, WV10 9QD, UK",
    "BT38 8GX - WG Buchanan": "WG Buchanan, 3 Sloefield Drive, Carrickfergus, BT38 8GX, UK",
    "WS10 8XL - AIB Foods site 2": "AIB Foods Site 2, Walsall, WS10 8XL, UK",
    "SO16 0YS - JDR": "JDR, Southampton, SO16 0YS, UK",
    "SO16 0YU - JDR": "JDR, Southampton, SO16 0YU, UK",
    "PE34 3LW - Golden Sunrise": "Golden Sunrise, Kings Lynn, PE34 3LW, UK",
    "S80 1RF - Withworth": "Withworth, Worksop, S80 1RF, UK",
}

HAULIERS = [
    ("Palletways","customer_care@palletways.com","UK Pallet"),
    ("TPN - The Pallet Network","mail@tpnmail.co.uk","UK Pallet"),
    ("Pall-Ex","info@pallex.com","UK Pallet / FTL"),
    ("Palletforce","info@palletforce.com","UK Pallet"),
    ("Armour Transport","enquiries@armourtransport.co.uk","Container"),
    ("Seven Logistics","bookings@seven-logistics.co.uk","Container"),
    ("Clintopia","info@clintopia.co.uk","Container"),
    ("Emirates Logistics","info@emirateslogistics.co.uk","Container"),
    ("Freightways","sales@freightways.co.uk","Container"),
    ("Jagelo Haulage","info@jhaulage.co.uk","Container"),
    ("Barrington Freight","sales@barringtonfreight.co.uk","NI / Ireland / Europe"),
    ("Direct Loads","info@directloads.co.uk","NI / Ireland"),
    ("Gemini Logistics","info@geminilogistics.co.uk","NI / Ireland"),
    ("Trailer Freight","info@trailerfreight.com","NI"),
    ("PW Freight","info@pwfreight.com","NI / Ireland"),
    ("LIF Lanigan","info@laniganfreight.com","NI / Ireland / Europe"),
]

# Top buttons - anchor navigation via tabs
tab1, tab2, tab3, tab4 = st.tabs(["📧 Container Email","🇬🇧 NI / Ireland Email","📦 UK Pallet Email","📩 All Haulier Emails"])

with tab1:
    st.subheader("Container Delivery Quote - Port to Warehouse")
    c1,c2 = st.columns(2)
    with c1:
        container_no = st.text_input("Container Number", "ZCSU6684045")
        size = st.selectbox("Size", ["40 FT","20 FT","40 FT HC"], index=0)
        product = st.text_input("Product", "Date Syrup")
        net_w = st.number_input("Net Weight MT", value=24.0)
        gross_w = st.number_input("Gross Weight MT", value=25.3)
        port = st.selectbox("Collection Port", ["London Gateway","Felixstowe","Southampton"])
        line = st.text_input("Shipping Line", "ZIM")
    with c2:
        date = st.text_input("Delivery Date", "19.10.2026")
        time = st.text_input("Slot Time", "8am")
        wh_key = st.selectbox("Delivery Warehouse", list(WAREHOUSES.keys()), index=1)
        to_email = st.text_input("Haulier Email (To)", "enquiries@armourtransport.co.uk")
    body1 = f"""Hi,

Can you please quote us for the delivery of the container:

Container: {container_no}
Size: {size}
Product: {product}
Weight: {net_w} MT - Gross {gross_w} MT
Collection Port: {port}
Shipping Line: {line}
Delivery Date & Time: {date} {time}
Delivery Address: {WAREHOUSES[wh_key]}

Regards,
Ali
Sahara UK Foods"""
    st.text_area("Live Preview - Email", body1, height=260)
    st.checkbox("✅ I have checked - approve to open in Outlook", key="chk1")
    if st.button("Open in Outlook - Container", key="btn1"):
        if not st.session_state.chk1:
            st.warning("Pehle checkbox tick karo - I have checked")
        else:
            subj = urllib.parse.quote(f"Container Delivery Quote - {container_no} - {port} to {wh_key}")
            link = f"mailto:{to_email}?subject={subj}&body={urllib.parse.quote(body1)}"
            st.markdown(f"[👉 Outlook me Kholo - Click Here]({link})")
            st.info("Email auto-send NAHI hogi. Outlook khulega, aap khud Send daboge.")

with tab2:
    st.subheader("NI / Ireland Pallet - 1 ya 2 Collection Points")
    mode = st.radio("Collection Mode", ["2 Collection Points","1 Collection Point"])
    c1,c2 = st.columns(2)
    with c1:
        prod1 = st.text_input("Collection 1 - Product", "Chopped Aseel Dates")
        qty1 = st.number_input("Collection 1 - Pallets", value=15)
        col1 = st.selectbox("Collection 1 Address", list(WAREHOUSES.keys()), index=1)
        phone1 = st.text_input("Collection 1 Phone", "+44 1205 820248")
        email1 = st.text_input("Collection 1 Email", "office@masonbrothersnorthend.co.uk")
    with c2:
        if mode=="2 Collection Points":
            prod2 = st.text_input("Collection 2 - Product", "Pitted Aseel Dates")
            qty2 = st.number_input("Collection 2 - Pallets", value=11)
            col2 = st.selectbox("Collection 2 Address", list(WAREHOUSES.keys()), index=2)
        else:
            prod2=""; qty2=0; col2=""
    total_p = qty1 + (qty2 if mode=="2 Collection Points" else 0)
    del_key = st.selectbox("Delivery Address - NI", list(WAREHOUSES.keys()), index=8)
    del_email = st.text_input("Delivery Email", "aplatt@wgbuchanan.com")
    del_phone = st.text_input("Delivery Phone", "02893 357812")
    body2 = f"""Hi,

Can you please quote us for the following?

Product: Dates
Weight: 26 MT
Pallets: {total_p}
Dimension: 100*120*100
Pickup Date: TBC
Delivery Date: TBC

You need to pick the load from {'two points:' if mode=='2 Collection Points' else 'one point:'}

{prod1}
Quantity: {qty1} Pallets
Pick-up Address: {WAREHOUSES[col1]}
Phone: {phone1}
Email: {email1}
"""
    if mode=="2 Collection Points":
        body2 += f"""
{prod2}
Quantity: {qty2} Pallets
Pick-up Address: {WAREHOUSES[col2]}
"""
    body2 += f"""
Delivery Address:
{WAREHOUSES[del_key]}
{del_email}
Call: {del_phone}

Regards,
Ali"""
    st.text_area("Live Preview - NI Email", body2, height=320)
    st.checkbox("✅ I have checked - approve", key="chk2")
    if st.button("Open in Outlook - NI", key="btn2"):
        if not st.session_state.chk2:
            st.warning("Pehle checkbox tick karo")
        else:
            link = f"mailto:?subject={urllib.parse.quote('Quote - NI / Ireland Pallet Delivery')}&body={urllib.parse.quote(body2)}"
            st.markdown(f"[👉 Outlook me Kholo]({link})")

with tab3:
    st.subheader("UK Pallet Movement to Client")
    c1,c2 = st.columns(2)
    with c1:
        to_name = st.text_input("To Name", "Mark")
        del_date = st.text_input("Delivery Date", "5th Nov")
        rotation = st.text_input("Rotation / Pallet Number", "0700697 (48 Cartons)")
        cont_ref = st.text_input("Container Ref No", "HLBU9466308")
        code = st.text_input("Sahara Product Code", "SUFL7251")
        desc = st.text_input("Description", "Org. Chopped Aseel Dates")
    with c2:
        lot = st.text_input("Lot No", "2151/AACHRF")
        qty = st.text_input("Quantity", "48 Cartons of 10Kg each /480kg/0.48MT")
        pallets = st.number_input("Pallets", value=1)
        po = st.text_input("PO Number", "12196")
        coll = st.selectbox("Collection Warehouse", list(WAREHOUSES.keys()), index=1)
        client = st.text_input("Client Name", "Food Republic")
        client_addr = st.text_area("Client Delivery Address", "Unit 3 Stewarts Lane Depot, Silverthorne Road, Battersea, London, SW8 3HE")
        client_email = st.text_input("Client Email", "JOE@FOOD-REPUBLIC.COM")
    body3 = f"""Hi {to_name},

Can you please quote us for the delivery below to our client on {del_date}?

Rotation/Pallet number: {rotation}
Container Ref No: {cont_ref}
Sahara Product Code: {code}
Description of Goods: {desc}
Lot No: {lot}
Quantity: {qty}
Pallet: {pallets} Pallet
PO Number: {po}
Collection: {WAREHOUSES[coll]}

Delivery Address:
{client}
{client_addr}

Email: {client_email}

Regards,
Ali"""
    st.text_area("Live Preview - UK Pallet Email", body3, height=300)
    st.checkbox("✅ I have checked - approve", key="chk3")
    if st.button("Open in Outlook - UK Pallet", key="btn3"):
        if not st.session_state.chk3:
            st.warning("Pehle checkbox tick karo")
        else:
            link = f"mailto:{client_email}?subject={urllib.parse.quote(f'Quote - Pallet Delivery to {client} - {del_date}')}&body={urllib.parse.quote(body3)}"
            st.markdown(f"[👉 Outlook me Kholo]({link})")

with tab4:
    st.subheader("All Haulier Emails - Copy karke contact karo")
    for name, email, typ in HAULIERS:
        colA,colB,colC = st.columns([3,3,2])
        colA.write(f"**{name}**")
        colB.code(email)
        colC.write(typ)
    st.info("Tip: Email select karke Ctrl+C se copy karo, ya Outlook me paste karo.")
    st.markdown("### Warehouses")
    for k,v in WAREHOUSES.items():
        st.write(f"- **{k}** : {v}")
    st.markdown("### Ports")
    st.write("- Felixstowe | Southampton | London Gateway")
