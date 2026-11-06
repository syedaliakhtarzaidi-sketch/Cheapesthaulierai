
import streamlit as st
import urllib.parse, pandas as pd

st.set_page_config(page_title="Sahara UK Foods - Cheapest Haulier AI", layout="wide")
st.markdown("<h1 style='color:#E65100'>🧡 Sahara UK Foods — Cheapest Haulier AI</h1><p>Logistics Manager - Ali | 3 Ports • 14 Warehouses • Rates + Emails + Outlook</p>", unsafe_allow_html=True)

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
PORTS = ["Felixstowe","Southampton","London Gateway"]

# RATES DATABASE - editable base rates (market cheapest slabs, user can change)
if "rates" not in st.session_state:
    st.session_state.rates = pd.DataFrame([
        ["TPN - The Pallet Network","mail@tpnmail.co.uk","UK Pallet",42, "per pallet","Next Day"],
        ["Palletways","customer_care@palletways.com","UK Pallet",45, "per pallet","Next Day"],
        ["Pall-Ex","info@pallex.com","UK Pallet",44, "per pallet","Next Day"],
        ["Palletforce","info@palletforce.com","UK Pallet",46, "per pallet","Next Day"],
        ["Armour Transport","enquiries@armourtransport.co.uk","Container 40FT",420, "per container","Port to Warehouse"],
        ["Seven Logistics","bookings@seven-logistics.co.uk","Container 40FT",450, "per container","Port to Warehouse"],
        ["Clintopia","info@clintopia.co.uk","Container 40FT",430, "per container","Port to Warehouse"],
        ["Emirates Logistics","info@emirateslogistics.co.uk","Container 40FT",440, "per container","Port to Warehouse"],
        ["Freightways","sales@freightways.co.uk","Container 40FT",410, "per container","Port to Warehouse"],
        ["Barrington Freight","sales@barringtonfreight.co.uk","NI / Ireland Pallet",225, "per pallet","24-48h"],
        ["Direct Loads","info@directloads.co.uk","NI / Ireland Pallet",240, "per pallet","Dedicated"],
        ["Gemini Logistics","info@geminilogistics.co.uk","NI / Ireland Pallet",230, "per pallet","24h"],
        ["Pall-Ex Logistics","info@pallex.com","FTL Full Trailer",750, "per FTL","UK-wide"],
        ["Road Haulage Services","info@roadhaulageservices.com","FTL Full Trailer",820, "per FTL","UK-wide"],
        ["Palletways Europe","customer_care@palletways.com","UK to Europe Pallet",65, "per pallet","EU"],
        ["Barrington Freight EU","sales@barringtonfreight.co.uk","UK to Europe Pallet",70, "per pallet","EU"],
    ], columns=["Haulier","Email","Service","Rate £","Unit","Transit"])

tab_rates, tab1, tab2, tab3, tab4 = st.tabs(["💷 1. RATES DEKHO - Cheapest Nikalo","📧 2. Container Email","🇬🇧 3. NI / Ireland Email","📦 4. UK Pallet Email","📩 5. All Haulier Emails"])

with tab_rates:
    st.subheader("Step 1: Pehle Rates Dekho - Phir Email Karo")
    st.info("👉 Kaise kaam karta hai: Neeche From / To / Pallets / Weight dalo → Sabse sasta haulier uppar aa jayega → Uske neeche wale 'Email This Haulier' button se usi rate ke saath email ban jayegi. Product / Weight / Pallets har dafa change ho sakte hain, rate auto-update ho jayega.")
    colA,colB,colC,colD = st.columns(4)
    with colA:
        from_loc = st.selectbox("From", PORTS + list(WAREHOUSES.keys()) + ["✏️ Custom - Client / Other Address (Neeche Likho)"], index=3)
        if from_loc.startswith("✏️"):
            from_loc = st.text_input("From - Custom Address Likho", "PE2 7LB - JSD warehouse")
        service = st.selectbox("Service Type", ["UK Pallet","Container 40FT","NI / Ireland Pallet","FTL Full Trailer","UK to Europe Pallet"])
    with colB:
        to_loc = st.selectbox("To", list(WAREHOUSES.keys()) + ["✏️ Custom - Client Address (Neeche Likho - e.g. Food Republic, Battersea)"], index=1)
        if to_loc.startswith("✏️"):
            to_loc = st.text_input("To - Client Address Likho", "Food Republic, Unit 3 Stewarts Lane Depot, Silverthorne Road, Battersea, London, SW8 3HE")
    with colC:
        pallets = st.number_input("No. of Pallets (agar pallet hai)", min_value=1, value=1)
        weight = st.number_input("Total Weight MT", min_value=0.1, value=0.48)
    with colD:
        product_r = st.text_input("Product (email me jayega)", "Org. Chopped Aseel Dates")
        st.write("")

    # Filter rates by service
    filtered = st.session_state.rates[st.session_state.rates["Service"]==service].copy()
    # Calculate total
    if "Pallet" in service:
        filtered["Total £"] = filtered["Rate £"] * pallets
    elif "Container" in service:
        filtered["Total £"] = filtered["Rate £"]
    elif "FTL" in service:
        filtered["Total £"] = filtered["Rate £"]
    filtered = filtered.sort_values("Total £")
    filtered["From"] = from_loc
    filtered["To"] = to_loc
    filtered["Product"] = product_r

    st.markdown("### 🏆 Cheapest to Expensive - Rates Table")
    st.dataframe(filtered[["Haulier","Email","Service","Rate £","Unit","Total £","Transit"]], use_container_width=True)

    if len(filtered)>0:
        cheapest = filtered.iloc[0]
        st.success(f"✅ SABSE SASTA: {cheapest['Haulier']} — £{cheapest['Total £']:.0f} total ({pallets} x £{cheapest['Rate £']}) — Email: {cheapest['Email']}")
        st.session_state["chosen_haulier"] = cheapest["Haulier"]
        st.session_state["chosen_email"] = cheapest["Email"]
        st.session_state["chosen_total"] = float(cheapest["Total £"])
        st.session_state["chosen_service"] = service
        st.session_state["chosen_from"] = from_loc
        st.session_state["chosen_to"] = to_loc
        st.session_state["chosen_product"] = product_r
        st.session_state["chosen_pallets"] = pallets
        st.session_state["chosen_weight"] = weight

        if st.button(f"➡️ Is Saste Haulier Ko Email Karo - {cheapest['Haulier']}"):
            st.info("Ab neeche wale Tabs (2,3,4) me jao — To me yehi haulier ka email auto aa jayega. Wahan product/weight/pallets badal kar email banao.")

    st.markdown("### ✏️ Rates Update Karo (Jab Naya Quote Aaye)")
    st.write("Agar kisi haulier ne naya rate diya hai to yahan badal do, agle dafa se wahi rate dikhega:")
    edited = st.data_editor(st.session_state.rates, num_rows="dynamic", use_container_width=True, key="rate_editor")
    if st.button("Save Rates"):
        st.session_state.rates = edited
        st.success("Rates save ho gaye!")

with tab1:
    st.subheader("Container Delivery Quote")
    # Pre-fill from rates tab if chosen
    def_email = st.session_state.get("chosen_email","enquiries@armourtransport.co.uk") if st.session_state.get("chosen_service")=="Container 40FT" else "enquiries@armourtransport.co.uk"
    c1,c2 = st.columns(2)
    with c1:
        container_no = st.text_input("Container Number", "ZCSU6684045")
        size = st.selectbox("Size", ["40 FT","20 FT","40 FT HC"])
        product = st.text_input("Product", st.session_state.get("chosen_product","Date Syrup"))
        net_w = st.number_input("Net Weight MT", value=24.0)
        gross_w = st.number_input("Gross Weight MT", value=25.3)
        port = st.selectbox("Collection Port", PORTS, index=2)
        line = st.text_input("Shipping Line", "ZIM")
    with c2:
        date = st.text_input("Delivery Date", "19.10.2026")
        time = st.text_input("Slot Time", "8am")
        wh_key = st.selectbox("Delivery Warehouse", list(WAREHOUSES.keys()), index=1)
        to_email = st.text_input("Haulier Email (To) - Rates tab se auto aaya", def_email)
        ref_rate = st.text_input("Rate Reference (optional)", f"Your quoted rate £{st.session_state.get('chosen_total','')} - please confirm" if st.session_state.get("chosen_total") else "")
    body1 = f"""Hi,

Can you please quote / confirm us for the delivery of the container:

Container: {container_no}
Size: {size}
Product: {product}
Weight: {net_w} MT - Gross {gross_w} MT
Collection Port: {port}
Shipping Line: {line}
Delivery Date & Time: {date} {time}
Delivery Address: {WAREHOUSES[wh_key]}
Rate Reference: {ref_rate}

Regards,
Ali
Sahara UK Foods"""
    st.text_area("Live Preview", body1, height=280)
    st.checkbox("✅ I have checked - approve", key="chk1")
    if st.button("Open in Outlook - Container"):
        if not st.session_state.chk1:
            st.warning("Pehle checkbox tick karo")
        else:
            link = f"mailto:{to_email}?subject={urllib.parse.quote(f'Container Delivery Quote - {container_no} - {port} to {wh_key}')}&body={urllib.parse.quote(body1)}"
            st.markdown(f"[👉 Outlook me Kholo]({link})")

with tab2:
    st.subheader("NI / Ireland Pallet")
    mode = st.radio("Collection Mode", ["2 Collection Points","1 Collection Point"])
    c1,c2 = st.columns(2)
    with c1:
        prod1 = st.text_input("Collection 1 - Product", "Chopped Aseel Dates")
        qty1 = st.number_input("Collection 1 - Pallets", value=15)
        col1 = st.selectbox("Collection 1 Address", list(WAREHOUSES.keys()), index=1)
    with c2:
        if mode=="2 Collection Points":
            prod2 = st.text_input("Collection 2 - Product", "Pitted Aseel Dates")
            qty2 = st.number_input("Collection 2 - Pallets", value=11)
            col2 = st.selectbox("Collection 2 Address", list(WAREHOUSES.keys()), index=2)
        else:
            prod2=""; qty2=0; col2=""
    total_p = qty1 + (qty2 if mode=="2 Collection Points" else 0)
    del_key = st.selectbox("Delivery - NI", list(WAREHOUSES.keys()), index=8)
    to_email2 = st.text_input("Haulier Email", st.session_state.get("chosen_email","sales@barringtonfreight.co.uk") if st.session_state.get("chosen_service")=="NI / Ireland Pallet" else "sales@barringtonfreight.co.uk")
    body2 = f"""Hi,

Can you please quote us for the following?

Product: Dates - {prod1} / {prod2}
Weight: {st.session_state.get('chosen_weight',26)} MT
Pallets: {total_p}
Dimension: 100*120*100
Pickup Date: TBC
Delivery Date: TBC
Rate Reference: £{st.session_state.get('chosen_total','')} - please confirm

Collections:
{prod1} - {qty1} Pallets - {WAREHOUSES[col1]}
"""
    if mode=="2 Collection Points":
        body2 += f"{prod2} - {qty2} Pallets - {WAREHOUSES[col2]}\n"
    body2 += f"""
Delivery: {WAREHOUSES[del_key]}
Regards, Ali"""
    st.text_area("Live Preview - NI", body2, height=300)
    st.checkbox("✅ I have checked", key="chk2")
    if st.button("Open in Outlook - NI"):
        if not st.session_state.chk2: st.warning("Tick karo")
        else:
            link = f"mailto:{to_email2}?subject={urllib.parse.quote('Quote - NI / Ireland Pallet')}&body={urllib.parse.quote(body2)}"
            st.markdown(f"[👉 Outlook me Kholo]({link})")

with tab3:
    st.subheader("UK Pallet Movement to Client")
    c1,c2 = st.columns(2)
    with c1:
        to_name = st.text_input("To Name", "Mark")
        del_date = st.text_input("Delivery Date", "5th Nov")
        rotation = st.text_input("Rotation", "0700697 (48 Cartons)")
        cont_ref = st.text_input("Container Ref", "HLBU9466308")
        code = st.text_input("Sahara Code", "SUFL7251")
        desc = st.text_input("Description", st.session_state.get("chosen_product","Org. Chopped Aseel Dates"))
    with c2:
        lot = st.text_input("Lot No", "2151/AACHRF")
        qty = st.text_input("Quantity", "48 Cartons of 10Kg each /480kg/0.48MT")
        pallets3 = st.number_input("Pallets", value=int(st.session_state.get("chosen_pallets",1)))
        po = st.text_input("PO Number", "12196")
        coll = st.selectbox("Collection Warehouse", list(WAREHOUSES.keys()), index=1)
        client = st.text_input("Client Name", "Food Republic")
        client_addr = st.text_area("Client Address", "Unit 3 Stewarts Lane Depot, Silverthorne Road, Battersea, London, SW8 3HE")
        client_email = st.text_input("Client Email", "JOE@FOOD-REPUBLIC.COM")
    haulier_email3 = st.text_input("Haulier Email (agar haulier ko bhejni hai)", st.session_state.get("chosen_email",""))
    body3 = f"""Hi {to_name},

Can you please quote us for the delivery below to our client on {del_date}?

Rotation/Pallet number: {rotation}
Container Ref No: {cont_ref}
Sahara Product Code: {code}
Description: {desc}
Lot No: {lot}
Quantity: {qty}
Pallet: {pallets3} Pallet
PO Number: {po}
Collection: {WAREHOUSES[coll]}
Rate Reference: £{st.session_state.get('chosen_total','')} - please confirm

Delivery:
{client}
{client_addr}
Email: {client_email}

Regards, Ali"""
    st.text_area("Live Preview - UK Pallet", body3, height=300)
    st.checkbox("✅ I have checked", key="chk3")
    if st.button("Open in Outlook - UK Pallet"):
        if not st.session_state.chk3: st.warning("Tick karo")
        else:
            to_final = haulier_email3 if haulier_email3 else client_email
            link = f"mailto:{to_final}?subject={urllib.parse.quote(f'Quote - Pallet to {client} - {del_date}')}&body={urllib.parse.quote(body3)}"
            st.markdown(f"[👉 Outlook me Kholo]({link})")

with tab4:
    st.subheader("All Haulier Emails")
    st.dataframe(st.session_state.rates[["Haulier","Email","Service","Rate £","Unit"]], use_container_width=True)
    st.write("Warehouses:")
    for k,v in WAREHOUSES.items():
        st.write(f"- {k} : {v}")
