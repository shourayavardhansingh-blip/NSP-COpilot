"""
Script to generate the complete BIS dataset for BIS AI Copilot:
- schemes.json (12 certification schemes)
- standards.json (55+ Indian Standards)
- qcos.json (18 Quality Control Orders)
- laboratories.json (35+ Laboratories with geo coordinates & scopes)
"""

import json
from pathlib import Path

SEED_DIR = Path(__file__).resolve().parent

# ==========================================
# 1. SCHEMES
# ==========================================
SCHEMES = [
    {
        "code": "SCHEME-I",
        "name": "Scheme-I (ISI Mark - Product Certification Scheme)",
        "description": "Flagship product certification scheme of BIS under Schedule-II of BIS (Conformity Assessment) Regulations 2018. Confers the right to use the Standard Mark (ISI Mark) upon verification of factory manufacturing infrastructure, quality control systems, in-house testing capability, and conformity of product samples tested in BIS/NABL recognized laboratories.",
        "applicable_to": "All industrial, electrical, civil, mechanical, chemical, food, and consumer goods covered by Indian Standards. Mandatory for products notified under central government Quality Control Orders (QCOs).",
        "process_summary": "1. Application submission on Manakonline portal with Form-I, factory layout, machinery list, and test equipment list.\n2. Verification of document completeness and payment of application fees.\n3. Preliminary factory inspection by BIS technical auditing officers to verify manufacturing capability and quality testing.\n4. Drawing of independent factory samples for complete compliance testing in BIS or recognized testing laboratories.\n5. Grant of Licence (GoL) upon satisfactory test report and submission of bank guarantee.\n6. Post-grant surveillance through factory and market sample surveillance audits.",
        "fee_structure": "Application Fee: ₹1,000 | Inspection Charges: ₹7,000 per man-day | Annual Minimum Marking Fee: ₹1,000 to ₹1,50,000 depending on product scale | Special 50% concession for Micro enterprises and 20% concession for Small enterprises under DPIIT guidelines.",
        "validity_years": 2,
        "is_mandatory_default": False,
        "official_guideline_url": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/certification_schemes/scheme_1"
    },
    {
        "code": "SCHEME-II",
        "name": "Scheme-II (Compulsory Registration Scheme - CRS)",
        "description": "Simplified registration scheme established under Schedule-II of BIS (Conformity Assessment) Regulations 2018, primarily notified by the Ministry of Electronics and Information Technology (MeitY) and the Ministry of New and Renewable Energy (MNRE). Based on manufacturer declaration of conformity supported by independent type-test reports from BIS-recognized laboratories, without mandatory pre-grant factory inspections.",
        "applicable_to": "Electronics, Information Technology Goods, Audio/Visual equipment, Solar Photovoltaic modules, Solar inverters, Storage batteries, and Smart Energy Meters notified under Compulsory Registration Orders.",
        "process_summary": "1. Product type-testing in a BIS-recognized accredited testing laboratory according to the applicable Indian Standard.\n2. Receipt of valid Laboratory Test Report (valid for 90 days for registration submission).\n3. Online application submission on the BIS CRS portal (www.crsbis.in) with test report, Form-I, trademark authorization, and undertaking.\n4. Document and test report scrutiny by BIS CRS officers.\n5. Grant of Registration and allocation of unique R-Number (e.g., R-XXXXXXXX).\n6. Manufacturer affixes the Standard Mark with R-Number and applicable IS number on product label and packaging.",
        "fee_structure": "Processing Fee: ₹10,000 to ₹50,000 per application depending on product category | Testing charges paid directly to testing laboratory | Renewal fee: ₹10,000 per year.",
        "validity_years": 2,
        "is_mandatory_default": True,
        "official_guideline_url": "https://www.crsbis.in/BIS/guidelines.do"
    },
    {
        "code": "SCHEME-IV",
        "name": "Scheme-IV (Certificate of Conformity - CoC)",
        "description": "Conformity assessment scheme where a Certificate of Conformity is granted for a specific batch, consignment, or discrete lot of manufactured goods based on sample testing, lot inspection, or specialized compliance criteria where ongoing factory certification is not required.",
        "applicable_to": "Specialized machinery, one-time imported consignments, composite materials, pressure vessels, and products where batch-wise verification is legally prescribed.",
        "process_summary": "1. Submission of application with batch details, invoice, and bill of lading.\n2. Sampling of consignment by BIS authorized inspectors.\n3. Laboratory testing of batch samples against standard specifications.\n4. Grant of Certificate of Conformity for the specified lot upon compliance.",
        "fee_structure": "Consignment inspection fee: ₹15,000 + testing charges at actuals.",
        "validity_years": 1,
        "is_mandatory_default": False,
        "official_guideline_url": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/certification_schemes/scheme_4"
    },
    {
        "code": "SCHEME-X",
        "name": "Scheme-X (Capital Goods & Industrial Machinery Certification)",
        "description": "Conformity assessment framework tailored for custom-built, heavy industrial machinery, capital goods, electrical switchgear assemblies, and specialized plant equipment manufactured in low batch quantities.",
        "applicable_to": "Heavy engineering equipment, transformers exceeding 2500 kVA, turbine components, and industrial process machinery.",
        "process_summary": "1. Comprehensive design appraisal and factory quality manual review.\n2. Factory audit of fabrication and non-destructive examination (NDE) procedures.\n3. Type test witnessing on representative production units.\n4. Grant of Scheme-X Licence.",
        "fee_structure": "Audit fee: ₹10,000/man-day + technical design review fee ₹25,000.",
        "validity_years": 3,
        "is_mandatory_default": False,
        "official_guideline_url": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/certification_schemes/scheme_10"
    },
    {
        "code": "SCHEME-XI",
        "name": "Scheme-XI (Mandatory Hallmarking for Gold & Silver)",
        "description": "Mandatory conformity scheme governing the purity certification and unique identification of gold and silver jewellery and artefacts under the Bureau of Indian Standards (Hallmarking) Regulations 2018.",
        "applicable_to": "Gold jewellery, gold artefacts (14K, 18K, 20K, 22K, 23K, 24K), silver jewellery, and silver bullion manufactured, wholesaled, or retailed in notified hallmarking districts across India.",
        "process_summary": "1. Jeweller registers online on Manakonline portal (zero registration fee for life).\n2. Jeweller sends unmarked jewellery items to a BIS-recognized Assaying and Hallmarking Centre (AHC).\n3. AHC performs XRF preliminary screening and fire assay (cupellation) purity test.\n4. Laser engraving of the 3 mandatory hallmark symbols: BIS Logo, Purity in Carat/Fineness (e.g., 22K916), and 6-digit alphanumeric HUID (Hallmark Unique Identification).\n5. Upload of HUID records to central BIS Hallmarking database.",
        "fee_structure": "Jeweller Registration: Free (Lifetime) | Hallmarking Fee: ₹45 per gold article + GST | ₹35 per silver article + GST.",
        "validity_years": 5,
        "is_mandatory_default": True,
        "official_guideline_url": "https://www.manakonline.in/MANAK/hallmarkingHome"
    },
    {
        "code": "FMCS",
        "name": "Foreign Manufacturers Certification Scheme (FMCS)",
        "description": "Specialized certification scheme operated by BIS since 2000 enabling overseas manufacturers situated outside India to obtain a BIS Licence to use the Standard ISI Mark on products exported to the Indian market.",
        "applicable_to": "All foreign manufacturers whose products fall under mandatory QCOs or who voluntarily seek the ISI mark for Indian market access.",
        "process_summary": "1. Foreign manufacturer appoints an Authorized Indian Representative (AIR) residing in India.\n2. Online application submission with factory layout, test equipment calibration certificates, and raw material specs.\n3. Payment of inspection fees, travel, accommodation, and per-diem for BIS auditing officers.\n4. Onsite audit of overseas manufacturing plant and drawing of independent verification samples.\n5. Testing of samples in BIS-approved Indian laboratories.\n6. Grant of Licence upon satisfactory test report and submission of Performance Bank Guarantee (PBG) of USD 10,000.",
        "fee_structure": "Application Fee: USD 1,000 | Inspection Charges: USD 7,000 per auditor + travel costs | Annual Licence Fee: USD 1,000 | Marking fee based on production volume | PBG: USD 10,000.",
        "validity_years": 2,
        "is_mandatory_default": False,
        "official_guideline_url": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/certification_schemes/fmcs"
    },
    {
        "code": "ECO-MARK",
        "name": "Eco Mark Scheme (Environmental Labeling)",
        "description": "Ecolabeling scheme administered by BIS in collaboration with the Ministry of Environment, Forest and Climate Change (MoEFCC) to certify consumer products that meet high environmental performance standards along with quality criteria.",
        "applicable_to": "Soaps, detergents, architectural paints, paper, plastics, batteries, cosmetics, textiles, lubricating oils, and packaging materials.",
        "process_summary": "1. Product must first satisfy all quality and safety requirements of the applicable Indian Standard under Scheme-I.\n2. Independent testing for environmental criteria (biodegradability, absence of heavy metals, low VOC, recyclable packaging).\n3. Grant of combined ISI + Earthen Pot (Matka) Eco Mark logo.",
        "fee_structure": "Scheme-I fees + ₹5,000 additional eco-criteria assessment fee.",
        "validity_years": 2,
        "is_mandatory_default": False,
        "official_guideline_url": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/certification_schemes/ecomark"
    },
    {
        "code": "QMS-9001",
        "name": "Quality Management Systems Certification (IS/ISO 9001)",
        "description": "Management systems certification validating that an organization adheres to structured quality management principles, customer focus, process approach, continual improvement, and evidence-based decision making.",
        "applicable_to": "All organizations, manufacturing plants, service providers, healthcare facilities, and educational institutions.",
        "process_summary": "1. Stage 1 adequacy audit of quality manual, process definitions, and internal audit records.\n2. Stage 2 comprehensive onsite implementation audit.\n3. Non-conformance closure and verification.\n4. Grant of 3-year ISO 9001 certification under BIS accreditation.",
        "fee_structure": "Application Fee: ₹15,000 | Audit charges: ₹10,000 per man-day.",
        "validity_years": 3,
        "is_mandatory_default": False,
        "official_guideline_url": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/certification_schemes/mscd"
    },
    {
        "code": "EMS-14001",
        "name": "Environmental Management Systems Certification (IS/ISO 14001)",
        "description": "Certifies that an enterprise has systematically identified and mitigated environmental impacts, complies with environmental legislation, prevents pollution, and minimizes waste generation across its lifecycle.",
        "applicable_to": "Chemical processing facilities, heavy manufacturing, construction enterprises, mining, and service organizations.",
        "process_summary": "1. Review of Environmental Aspects and Impacts register and legal register.\n2. Stage 1 and Stage 2 onsite environmental audits by certified BIS auditors.\n3. Certification grant with annual surveillance audits.",
        "fee_structure": "Application Fee: ₹15,000 | Audit charges: ₹10,000 per man-day.",
        "validity_years": 3,
        "is_mandatory_default": False,
        "official_guideline_url": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/certification_schemes/mscd"
    },
    {
        "code": "FSMS-22000",
        "name": "Food Safety Management Systems Certification (IS/ISO 22000)",
        "description": "Combines ISO management framework with Hazard Analysis and Critical Control Point (HACCP) principles and prerequisite programmes to assure food safety across the farm-to-fork supply chain.",
        "applicable_to": "Food processing plants, packaged beverage bottling plants, cold storage operators, dairy processors, and catering facilities.",
        "process_summary": "1. HACCP plan evaluation and prerequisite programme audit.\n2. Stage 1 and Stage 2 food safety audits including microbiological validation.\n3. Grant of FSMS certificate.",
        "fee_structure": "Application Fee: ₹20,000 | Audit charges: ₹12,000 per man-day.",
        "validity_years": 3,
        "is_mandatory_default": False,
        "official_guideline_url": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/certification_schemes/mscd"
    },
    {
        "code": "ISMS-27001",
        "name": "Information Security Management Systems Certification (IS/ISO/IEC 27001)",
        "description": "Validates the establishment, implementation, maintenance, and continual improvement of an organization-wide Information Security Management System covering data confidentiality, integrity, and availability.",
        "applicable_to": "IT enterprises, data centres, fintech companies, cloud service providers, and telecommunications operators.",
        "process_summary": "1. Statement of Applicability (SoA) and risk assessment methodology review.\n2. Technical controls and information asset protection audit.\n3. Certification grant with surveillance every 12 months.",
        "fee_structure": "Application Fee: ₹25,000 | Audit charges: ₹15,000 per man-day.",
        "validity_years": 3,
        "is_mandatory_default": False,
        "official_guideline_url": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/certification_schemes/mscd"
    },
    {
        "code": "OHSMS-45001",
        "name": "Occupational Health and Safety Management Systems (IS/ISO 45001)",
        "description": "Enables organizations to provide safe and healthy workplaces by preventing work-related injury and ill health, as well as by proactively improving its occupational health and safety performance.",
        "applicable_to": "Construction companies, industrial manufacturing plants, refineries, logistics, and infrastructure developers.",
        "process_summary": "1. Hazard identification and risk analysis (HIRA) review.\n2. Onsite safety protocol, emergency response, and operational control verification.\n3. Certification award with annual surveillance.",
        "fee_structure": "Application Fee: ₹18,000 | Audit charges: ₹10,000 per man-day.",
        "validity_years": 3,
        "is_mandatory_default": False,
        "official_guideline_url": "https://www.services.bis.gov.in/php/BIS_2.0/bisconnect/knowyourstandards/certification_schemes/mscd"
    }
]

# Read standards from standards.json previously generated
with open(SEED_DIR / "standards.json", "r", encoding="utf-8") as f:
    STANDARDS = json.load(f)

# ==========================================
# 2. QUALITY CONTROL ORDERS (18 QCOs)
# ==========================================
QCOS = [
    {
        "order_number": "S.O. 853(E) / 2020",
        "title": "Toys (Quality Control) Order, 2020",
        "issuing_ministry": "Ministry of Commerce and Industry (DPIIT)",
        "product_category": "Toys and Childcare Goods",
        "gazette_date": "2020-02-25",
        "enforcement_date": "2021-01-01",
        "status": "In Force",
        "official_url": "https://dpiit.gov.in/sites/default/files/Toys_Quality_Control_Order_2020.pdf",
        "is_fixture": False,
        "notes": "Mandates that all non-electric and electric toys manufactured, imported, or sold in India must conform to relevant Indian Standards (IS 9873 Parts 1, 2, 3 and IS 15644) and bear the Standard ISI Mark under Scheme-I of Schedule-II of the BIS (Conformity Assessment) Regulations 2018. Goods manufactured by registered artisans and weavers are subject to special MSME provisions.",
        "standards": [
            {"is_number": "IS 9873 (Part 1): 2019", "exemption_notes": "Mandatory for physical and mechanical properties"},
            {"is_number": "IS 9873 (Part 2): 2017", "exemption_notes": "Mandatory for flammability"},
            {"is_number": "IS 9873 (Part 3): 2020", "exemption_notes": "Mandatory for toxic heavy metal migration"},
            {"is_number": "IS 15644: 2006", "exemption_notes": "Mandatory for all electric toys"}
        ],
        "amendments": [
            {
                "amendment_number": "Toys (Quality Control) Amendment Order, 2020",
                "gazette_notification": "S.O. 3144(E)",
                "notification_date": "2020-09-15",
                "effective_date": "2021-01-01",
                "summary": "Extended original enforcement date from 01-09-2020 to 01-01-2021 to allow manufacturers and testing laboratories to upgrade capacity.",
                "source_url": "https://dpiit.gov.in/"
            }
        ]
    },
    {
        "order_number": "S.O. 1109(E) / 2023",
        "title": "Electrical Appliances for Household and Similar Purposes (Quality Control) Order, 2023",
        "issuing_ministry": "Ministry of Commerce and Industry (DPIIT)",
        "product_category": "Household Electrical Appliances",
        "gazette_date": "2023-03-05",
        "enforcement_date": "2024-03-01",
        "status": "In Force",
        "official_url": "https://dpiit.gov.in/sites/default/files/Electrical_Appliances_QCO_2023.pdf",
        "is_fixture": False,
        "notes": "Mandates compulsory conformity to IS 302 series and standard mark (ISI Mark under Scheme-I) for stationary storage water heaters, electric irons, room heaters, immersion water heaters, and electric stoves.",
        "standards": [
            {"is_number": "IS 302 (Part 1): 2008", "exemption_notes": "General safety requirements"},
            {"is_number": "IS 302 (Part 2/Sec 3): 2007", "exemption_notes": "Electric irons"},
            {"is_number": "IS 302 (Part 2/Sec 21): 2011", "exemption_notes": "Stationary storage water heaters (geysers)"},
            {"is_number": "IS 302 (Part 2/Sec 30): 2007", "exemption_notes": "Room heaters"},
            {"is_number": "IS 302 (Part 2/Sec 201): 2008", "exemption_notes": "Immersion heaters"},
            {"is_number": "IS 302 (Part 2/Sec 14): 2009", "exemption_notes": "Kitchen machines and mixers"}
        ],
        "amendments": [
            {
                "amendment_number": "Electrical Appliances QCO (First Amendment) 2024",
                "gazette_notification": "S.O. 724(E)",
                "notification_date": "2024-02-15",
                "effective_date": "2024-09-01",
                "summary": "Granted staggered compliance extension: Small enterprises until 01-12-2024 and Micro enterprises until 01-03-2025.",
                "source_url": "https://dpiit.gov.in/"
            }
        ]
    },
    {
        "order_number": "S.O. 2920(E) / 2017",
        "title": "Solar Photovoltaics, Systems, Devices and Components Goods (Requirements for Compulsory Registration) Order, 2017",
        "issuing_ministry": "Ministry of New and Renewable Energy (MNRE)",
        "product_category": "Solar Energy Equipment",
        "gazette_date": "2017-09-05",
        "enforcement_date": "2018-09-05",
        "status": "In Force",
        "official_url": "https://mnre.gov.in/solar-photovoltaics-quality-control-order",
        "is_fixture": False,
        "notes": "Mandates compulsory registration under Scheme-II (CRS) with BIS for crystalline silicon terrestrial PV modules, thin-film modules, PV grid-tie inverters, and storage batteries used in solar projects.",
        "standards": [
            {"is_number": "IS 14286: 2010", "exemption_notes": "Crystalline silicon PV modules"},
            {"is_number": "IS/IEC 61730 (Part 1): 2004", "exemption_notes": "PV safety construction"},
            {"is_number": "IS/IEC 61730 (Part 2): 2004", "exemption_notes": "PV safety testing"},
            {"is_number": "IS 16221 (Part 2): 2015", "exemption_notes": "PV inverters"}
        ],
        "amendments": []
    },
    {
        "order_number": "S.O. 1387(E) / 2024",
        "title": "Steel and Steel Products (Quality Control) Order, 2024",
        "issuing_ministry": "Ministry of Steel",
        "product_category": "Iron and Steel",
        "gazette_date": "2024-03-18",
        "enforcement_date": "2024-09-18",
        "status": "In Force",
        "official_url": "https://steel.gov.in/steel-qco-2024",
        "is_fixture": False,
        "notes": "Consolidates and mandates ISI marking under Scheme-I for all structural steel, TMT rebars, carbon steel plates, seamless pipes, and galvanized sheets. Disallows commercial import or trade without valid BIS licence.",
        "standards": [
            {"is_number": "IS 1786: 2008", "exemption_notes": "High strength TMT rebars"},
            {"is_number": "IS 2062: 2011", "exemption_notes": "Structural steel"}
        ],
        "amendments": []
    },
    {
        "order_number": "S.O. 1266(E) / 2021",
        "title": "Electronics and Information Technology Goods (Requirement for Compulsory Registration) Order, 2021",
        "issuing_ministry": "Ministry of Electronics and Information Technology (MeitY)",
        "product_category": "Information Technology and Electronics",
        "gazette_date": "2021-03-18",
        "enforcement_date": "2021-10-01",
        "status": "In Force",
        "official_url": "https://www.meity.gov.in/esdm/standards",
        "is_fixture": False,
        "notes": "Covers 64+ product categories under Compulsory Registration Scheme (Scheme-II). Requires type testing in BIS-recognized labs and R-number allocation for smart phones, laptops, smart TVs, power banks, LED lights, and CCTV.",
        "standards": [
            {"is_number": "IS 13252 (Part 1): 2010", "exemption_notes": "IT equipment safety"},
            {"is_number": "IS 16333 (Part 3): 2022", "exemption_notes": "Language support for mobile phones"},
            {"is_number": "IS 616: 2017", "exemption_notes": "Audio and video equipment"},
            {"is_number": "IS 16046 (Part 2): 2018", "exemption_notes": "Lithium batteries and power banks"},
            {"is_number": "IS 15885 (Part 2/Sec 13): 2012", "exemption_notes": "LED drivers"},
            {"is_number": "IS 16102 (Part 1): 2012", "exemption_notes": "LED lamps"},
            {"is_number": "IS 16242 (Part 1): 2014", "exemption_notes": "UPS systems"}
        ],
        "amendments": []
    },
    {
        "order_number": "S.O. 4252(E) / 2020",
        "title": "Helmets for riders of Two-Wheeled Motor Vehicles (Quality Control) Order, 2020",
        "issuing_ministry": "Ministry of Commerce and Industry (DPIIT) & MoRTH",
        "product_category": "Personal Safety and Automotive Accessories",
        "gazette_date": "2020-11-26",
        "enforcement_date": "2021-06-01",
        "status": "In Force",
        "official_url": "https://dpiit.gov.in/sites/default/files/Two_Wheeler_Helmets_QCO_2020.pdf",
        "is_fixture": False,
        "notes": "Mandates compulsory ISI marking under Scheme-I for all two-wheeler protective helmets. Completely outlaws non-ISI helmets from manufacture, storage, and retail in India.",
        "standards": [
            {"is_number": "IS 4151: 2020", "exemption_notes": "Two-wheeler helmets"}
        ],
        "amendments": []
    },
    {
        "order_number": "S.O. 3838(E) / 2023",
        "title": "Plywood and Allied Products (Quality Control) Order, 2023",
        "issuing_ministry": "Ministry of Commerce and Industry (DPIIT)",
        "product_category": "Wood and Wood Products",
        "gazette_date": "2023-08-29",
        "enforcement_date": "2024-02-28",
        "status": "In Force",
        "official_url": "https://dpiit.gov.in/sites/default/files/Plywood_QCO_2023.pdf",
        "is_fixture": False,
        "notes": "Compulsory conformity to Indian Standards and ISI Mark under Scheme-I for marine plywood, general purpose plywood, wooden flush door shutters, and particle boards.",
        "standards": [
            {"is_number": "IS 710: 2010", "exemption_notes": "Marine plywood"},
            {"is_number": "IS 303: 1989", "exemption_notes": "General purpose plywood"},
            {"is_number": "IS 2202 (Part 1): 1999", "exemption_notes": "Wooden flush doors"}
        ],
        "amendments": [
            {
                "amendment_number": "Plywood QCO (Amendment) 2024",
                "gazette_notification": "S.O. 1198(E)",
                "notification_date": "2024-03-12",
                "effective_date": "2024-08-28",
                "summary": "Granted compliance timeline extensions for Micro and Small plywood enterprises to install mandatory formaldehyde and boiling water test equipment.",
                "source_url": "https://dpiit.gov.in/"
            }
        ]
    },
    {
        "order_number": "S.O. 2146(E) / 2022",
        "title": "Footwear made from all-Rubber and all-Polymeric Materials and its Components (Quality Control) Order, 2022",
        "issuing_ministry": "Ministry of Commerce and Industry (DPIIT)",
        "product_category": "Footwear and Leather Goods",
        "gazette_date": "2022-06-03",
        "enforcement_date": "2023-07-01",
        "status": "In Force",
        "official_url": "https://dpiit.gov.in/sites/default/files/Polymeric_Footwear_QCO_2022.pdf",
        "is_fixture": False,
        "notes": "Mandates ISI mark under Scheme-I for rubber Hawai chappals, PVC sandals, slippers, and rubber gumboots.",
        "standards": [
            {"is_number": "IS 6721: 2023", "exemption_notes": "PVC sandals and slippers"},
            {"is_number": "IS 10702: 2023", "exemption_notes": "Rubber Hawai chappal"}
        ],
        "amendments": []
    },
    {
        "order_number": "S.O. 2147(E) / 2022",
        "title": "Footwear made from Leather and other Materials (Quality Control) Order, 2022",
        "issuing_ministry": "Ministry of Commerce and Industry (DPIIT)",
        "product_category": "Footwear and Leather Goods",
        "gazette_date": "2022-06-03",
        "enforcement_date": "2023-07-01",
        "status": "In Force",
        "official_url": "https://dpiit.gov.in/sites/default/files/Leather_Footwear_QCO_2022.pdf",
        "is_fixture": False,
        "notes": "Mandatory conformity to IS 15298 series and ISI Mark under Scheme-I for industrial safety footwear, protective footwear, and occupational leather shoes.",
        "standards": [
            {"is_number": "IS 15298 (Part 2): 2016", "exemption_notes": "Safety footwear (200 J)"},
            {"is_number": "IS 15298 (Part 3): 2019", "exemption_notes": "Protective footwear (100 J)"}
        ],
        "amendments": []
    },
    {
        "order_number": "S.O. 981(E) / 2024",
        "title": "Cement (Quality Control) Order, 2024",
        "issuing_ministry": "Ministry of Commerce and Industry (DPIIT)",
        "product_category": "Cement and Construction Materials",
        "gazette_date": "2024-02-27",
        "enforcement_date": "2024-02-27",
        "status": "In Force",
        "official_url": "https://dpiit.gov.in/sites/default/files/Cement_QCO_2024.pdf",
        "is_fixture": False,
        "notes": "Re-notifies mandatory ISI marking under Scheme-I for all forms of cement manufactured, imported, or packed in bags in India.",
        "standards": [
            {"is_number": "IS 269: 2015", "exemption_notes": "OPC cement 33, 43, 53 grade"},
            {"is_number": "IS 1489 (Part 1): 2015", "exemption_notes": "Portland pozzolana cement fly-ash based"},
            {"is_number": "IS 455: 2015", "exemption_notes": "Portland slag cement"}
        ],
        "amendments": []
    },
    {
        "order_number": "S.O. 145(E) / 2021",
        "title": "Packaged Drinking Water and Natural Mineral Water (Quality Control) Order, 2021",
        "issuing_ministry": "Ministry of Health and Family Welfare (FSSAI) & MoCAFPD",
        "product_category": "Beverages and Packaged Water",
        "gazette_date": "2021-01-11",
        "enforcement_date": "2021-04-01",
        "status": "In Force",
        "official_url": "https://fssai.gov.in/packaged-water-regulations",
        "is_fixture": False,
        "notes": "Section 31 of FSS Act and BIS regulations mandate dual certification: No food business operator can produce or sell packaged water without both FSSAI licence and BIS ISI Mark licence.",
        "standards": [
            {"is_number": "IS 14543: 2016", "exemption_notes": "Packaged drinking water"},
            {"is_number": "IS 13428: 2005", "exemption_notes": "Packaged natural mineral water"}
        ],
        "amendments": []
    },
    {
        "order_number": "S.O. 402(E) / 2023",
        "title": "Distribution Transformers (Quality Control) Order, 2023",
        "issuing_ministry": "Ministry of Power",
        "product_category": "Heavy Electrical Equipment",
        "gazette_date": "2023-01-24",
        "enforcement_date": "2023-07-24",
        "status": "In Force",
        "official_url": "https://powermin.gov.in/distribution-transformers-qco",
        "is_fixture": False,
        "notes": "Mandates compulsory ISI marking under Scheme-I for all outdoor type oil-immersed distribution transformers up to 2500 kVA, 33 kV. Mandates maximum energy loss threshold compliance.",
        "standards": [
            {"is_number": "IS 1180 (Part 1): 2014", "exemption_notes": "Distribution transformers"}
        ],
        "amendments": []
    },
    {
        "order_number": "S.O. 531(E) / 2023",
        "title": "Room Air Conditioners and Hermetic Compressors (Quality Control) Order, 2023",
        "issuing_ministry": "Ministry of Commerce and Industry (DPIIT)",
        "product_category": "Air Conditioning and Refrigeration",
        "gazette_date": "2023-02-01",
        "enforcement_date": "2024-01-01",
        "status": "In Force",
        "official_url": "https://dpiit.gov.in/sites/default/files/AC_Compressors_QCO_2023.pdf",
        "is_fixture": False,
        "notes": "Mandates ISI mark under Scheme-I for room air conditioners (window and split) and hermetically sealed motor compressors used in domestic and commercial refrigeration.",
        "standards": [
            {"is_number": "IS 1391 (Part 1): 2017", "exemption_notes": "Unitary window ACs"},
            {"is_number": "IS 1391 (Part 2): 2018", "exemption_notes": "Split ACs"}
        ],
        "amendments": []
    },
    {
        "order_number": "S.O. 1620(E) / 2021",
        "title": "Domestic Gas Stoves and LPG Pressure Regulators (Quality Control) Order, 2021",
        "issuing_ministry": "Ministry of Commerce and Industry (DPIIT) & MoPNG",
        "product_category": "Domestic Appliances and Gas Fittings",
        "gazette_date": "2021-04-12",
        "enforcement_date": "2022-01-01",
        "status": "In Force",
        "official_url": "https://dpiit.gov.in/sites/default/files/LPG_Stoves_QCO_2021.pdf",
        "is_fixture": False,
        "notes": "Requires domestic pressure cookers, low pressure regulators, and LPG cylinders to strictly conform to Indian Standards and bear the ISI Mark.",
        "standards": [
            {"is_number": "IS 2347: 2017", "exemption_notes": "Domestic pressure cookers"},
            {"is_number": "IS 3196 (Part 1): 2013", "exemption_notes": "LPG cylinders"},
            {"is_number": "IS 9798: 1995", "exemption_notes": "LPG pressure regulators"}
        ],
        "amendments": []
    },
    {
        "order_number": "S.O. 2780(E) / 2023",
        "title": "Plugs and Sockets-Outlets and Smart Energy Meters (Quality Control) Order, 2023",
        "issuing_ministry": "Ministry of Commerce and Industry (DPIIT) & Ministry of Power",
        "product_category": "Electrical Accessories and Smart Grid",
        "gazette_date": "2023-06-20",
        "enforcement_date": "2024-03-01",
        "status": "In Force",
        "official_url": "https://dpiit.gov.in/sites/default/files/Plugs_Meters_QCO_2023.pdf",
        "is_fixture": False,
        "notes": "Requires all domestic plugs, socket-outlets, multi-plugs, and static direct connected watt-hour smart meters to carry the ISI mark under Scheme-I.",
        "standards": [
            {"is_number": "IS 1293: 2019", "exemption_notes": "Plugs and sockets"},
            {"is_number": "IS 16444 (Part 1): 2015", "exemption_notes": "Smart energy meters"}
        ],
        "amendments": []
    },
    {
        "order_number": "S.O. 3102(E) / 2023",
        "title": "Electric Ceiling Fans (Quality Control) Order, 2023",
        "issuing_ministry": "Ministry of Commerce and Industry (DPIIT)",
        "product_category": "Domestic Electrical Appliances",
        "gazette_date": "2023-08-09",
        "enforcement_date": "2024-09-01",
        "status": "In Force",
        "official_url": "https://dpiit.gov.in/sites/default/files/Ceiling_Fans_QCO_2023.pdf",
        "is_fixture": False,
        "notes": "Mandates compulsory ISI marking under Scheme-I for electric ceiling fans, including BEE star rating compliance.",
        "standards": [
            {"is_number": "IS 374: 2019", "exemption_notes": "Electric ceiling fans"}
        ],
        "amendments": []
    },
    {
        "order_number": "S.O. 205(E) / 2020",
        "title": "Mandatory Hallmarking of Gold Jewellery and Gold Artefacts Order, 2020",
        "issuing_ministry": "Department of Consumer Affairs (DCA)",
        "product_category": "Precious Metals and Jewellery",
        "gazette_date": "2020-01-15",
        "enforcement_date": "2021-06-16",
        "status": "In Force",
        "official_url": "https://consumeraffairs.nic.in/hallmarking-order-2020",
        "is_fixture": False,
        "notes": "Mandates compulsory hallmarking with 6-digit HUID code for all 14k, 18k, 20k, 22k, 23k, and 24k gold jewellery sold by registered jewellers across notified districts in India.",
        "standards": [
            {"is_number": "IS 1417: 2016", "exemption_notes": "Gold jewellery hallmarking"},
            {"is_number": "IS 2112: 2014", "exemption_notes": "Silver jewellery hallmarking"}
        ],
        "amendments": []
    },
    {
        "order_number": "S.O. 4118(E) / 2022",
        "title": "Caustic Soda and Industrial Chemicals (Quality Control) Order, 2022",
        "issuing_ministry": "Department of Chemicals and Petrochemicals (DCPC)",
        "product_category": "Industrial Chemicals",
        "gazette_date": "2022-09-12",
        "enforcement_date": "2023-04-12",
        "status": "In Force",
        "official_url": "https://chemicals.gov.in/caustic-soda-qco-2022",
        "is_fixture": False,
        "notes": "Prohibits manufacture, import, and sale of caustic soda and industrial methanol without BIS Licence and Standard ISI mark under Scheme-I.",
        "standards": [
            {"is_number": "IS 252: 2013", "exemption_notes": "Caustic soda pure and technical"},
            {"is_number": "IS 517: 2020", "exemption_notes": "Industrial methanol"}
        ],
        "amendments": []
    }
]

# ==========================================
# 3. LABORATORIES (38 Laboratories across India)
# ==========================================
LABORATORIES = [
    # --- BIS Owned Central, Regional & Branch Labs ---
    {
        "lab_code": "BIS-CL-001",
        "name": "Bureau of Indian Standards Central Laboratory (CL)",
        "address": "Plot No. 20/9, Site IV, Sahibabad Industrial Area, Ghaziabad",
        "city": "Ghaziabad",
        "district": "Ghaziabad",
        "state": "Uttar Pradesh",
        "pincode": "201010",
        "latitude": 28.6692,
        "longitude": 77.3538,
        "contact_person": "Scientist-G & Head of Central Laboratory, BIS",
        "phone": "+91-120-2771501",
        "email": "cl@bis.gov.in",
        "lab_type": "BIS Central Laboratory",
        "status": "Recognized",
        "recognition_valid_until": "2030-12-31",
        "source_url": "https://lims.bis.gov.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 302 (Part 1): 2008", "product_category": "Electrical Appliances", "testing_capability": "Complete electrical safety, insulation resistance, electric strength, earth resistance"},
            {"is_number": "IS 302 (Part 2/Sec 21): 2011", "product_category": "Water Heaters", "testing_capability": "Hydrostatic pressure testing up to 1.0 MPa, standing heat loss, energy consumption"},
            {"is_number": "IS 302 (Part 2/Sec 3): 2007", "product_category": "Electric Irons", "testing_capability": "Soleplate temperature measurement, thermal safety, drop test, cord endurance"},
            {"is_number": "IS 302 (Part 2/Sec 30): 2007", "product_category": "Room Heaters", "testing_capability": "Radiation safety, stability test, overturning switch response"},
            {"is_number": "IS 302 (Part 2/Sec 201): 2008", "product_category": "Immersion Heaters", "testing_capability": "Immersion depth safety, earth continuity, leakage current"},
            {"is_number": "IS 694: 2010", "product_category": "Cables and Wires", "testing_capability": "Conductor resistance, insulation resistance, spark test, flammability test"},
            {"is_number": "IS 1786: 2008", "product_category": "TMT Steel Bars", "testing_capability": "Yield strength, ultimate tensile strength, elongation, bend and rebend test"},
            {"is_number": "IS 9873 (Part 1): 2019", "product_category": "Toys", "testing_capability": "Mechanical and physical testing, sharp edges, drop test, tension test"},
            {"is_number": "IS 9873 (Part 3): 2020", "product_category": "Toys", "testing_capability": "Heavy metals ICP-OES migration test (Pb, Cd, As, Sb, Ba, Cr, Hg, Se)"},
            {"is_number": "IS 14543: 2016", "product_category": "Packaged Water", "testing_capability": "Complete physical, chemical, pesticide residue GC-MS, and microbiological pathogen analysis"}
        ]
    },
    {
        "lab_code": "BIS-WRL-002",
        "name": "Bureau of Indian Standards Western Regional Laboratory (WRL)",
        "address": "Manakalaya, E9, MIDC, Andheri (East), Mumbai",
        "city": "Mumbai",
        "district": "Mumbai Suburban",
        "state": "Maharashtra",
        "pincode": "400093",
        "latitude": 19.1197,
        "longitude": 72.8687,
        "contact_person": "Scientist-F & In-Charge, WRL",
        "phone": "+91-22-28329295",
        "email": "wrl@bis.gov.in",
        "lab_type": "BIS Regional Laboratory",
        "status": "Recognized",
        "recognition_valid_until": "2030-12-31",
        "source_url": "https://lims.bis.gov.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 302 (Part 1): 2008", "product_category": "Electrical Appliances", "testing_capability": "Electrical safety and performance testing"},
            {"is_number": "IS 15298 (Part 2): 2016", "product_category": "Safety Footwear", "testing_capability": "200 Joules toe impact, 15 kN compression, sole adhesion and oil resistance"},
            {"is_number": "IS 6721: 2023", "product_category": "PVC Footwear", "testing_capability": "Flex cracking, strap pull-out, hardness testing"},
            {"is_number": "IS 10702: 2023", "product_category": "Rubber Footwear", "testing_capability": "Tensile strength, elongation, split tear resistance"},
            {"is_number": "IS 14543: 2016", "product_category": "Packaged Water", "testing_capability": "Physicochemical and microbiological testing"},
            {"is_number": "IS 252: 2013", "product_category": "Chemicals", "testing_capability": "Assay of caustic soda, sodium carbonate and chloride determination"}
        ]
    },
    {
        "lab_code": "BIS-SRL-003",
        "name": "Bureau of Indian Standards Southern Regional Laboratory (SRL)",
        "address": "CIT Campus, IV Cross Road, Taramani, Chennai",
        "city": "Chennai",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "pincode": "600113",
        "latitude": 12.9863,
        "longitude": 80.2432,
        "contact_person": "Scientist-F & In-Charge, SRL",
        "phone": "+91-44-22541442",
        "email": "srl@bis.gov.in",
        "lab_type": "BIS Regional Laboratory",
        "status": "Recognized",
        "recognition_valid_until": "2030-12-31",
        "source_url": "https://lims.bis.gov.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 302 (Part 1): 2008", "product_category": "Electrical Appliances", "testing_capability": "Safety testing for household electrical appliances"},
            {"is_number": "IS 374: 2019", "product_category": "Ceiling Fans", "testing_capability": "Air delivery in wind tunnel test room, power factor, service value"},
            {"is_number": "IS 694: 2010", "product_category": "Cables and Wires", "testing_capability": "HV spark test, heat shock, elongation test"},
            {"is_number": "IS 269: 2015", "product_category": "Cement", "testing_capability": "Fineness, setting time, soundess, 3/7/28 day compressive strength"},
            {"is_number": "IS 1489 (Part 1): 2015", "product_category": "PPC Cement", "testing_capability": "Pozzolanic activity index, drying shrinkage"},
            {"is_number": "IS 14543: 2016", "product_category": "Packaged Water", "testing_capability": "Heavy metals and microbial water quality testing"}
        ]
    },
    {
        "lab_code": "BIS-ERL-004",
        "name": "Bureau of Indian Standards Eastern Regional Laboratory (ERL)",
        "address": "1/14 C.I.T. Scheme VII (M), VIP Road, Kankurgachi, Kolkata",
        "city": "Kolkata",
        "district": "Kolkata",
        "state": "West Bengal",
        "pincode": "700054",
        "latitude": 22.5802,
        "longitude": 88.3965,
        "contact_person": "Scientist-F & In-Charge, ERL",
        "phone": "+91-33-23207080",
        "email": "erl@bis.gov.in",
        "lab_type": "BIS Regional Laboratory",
        "status": "Recognized",
        "recognition_valid_until": "2030-12-31",
        "source_url": "https://lims.bis.gov.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 1786: 2008", "product_category": "TMT Steel Bars", "testing_capability": "Tensile stress, 1000 kN UTM testing, bend-rebend, rib area measurement"},
            {"is_number": "IS 2062: 2011", "product_category": "Structural Steel", "testing_capability": "Charpy impact V-notch test at 0°C and -20°C, yield strength"},
            {"is_number": "IS 710: 2010", "product_category": "Plywood", "testing_capability": "72-hour boiling water soak test, adhesive shear strength, moisture content"},
            {"is_number": "IS 303: 1989", "product_category": "Plywood", "testing_capability": "Moisture resistance, flexural strength, dry shear test"},
            {"is_number": "IS 14543: 2016", "product_category": "Packaged Water", "testing_capability": "Total dissolved solids, alkalinity, microbial pathogens"}
        ]
    },
    {
        "lab_code": "BIS-NRL-005",
        "name": "Bureau of Indian Standards Northern Regional Laboratory (NRL)",
        "address": "Plot No. 4A, Sector 27B, Madhya Marg, Chandigarh",
        "city": "Chandigarh",
        "district": "Chandigarh",
        "state": "Chandigarh",
        "pincode": "160019",
        "latitude": 30.7303,
        "longitude": 76.7981,
        "contact_person": "Scientist-F & In-Charge, NRL",
        "phone": "+91-172-2650206",
        "email": "nrl@bis.gov.in",
        "lab_type": "BIS Regional Laboratory",
        "status": "Recognized",
        "recognition_valid_until": "2030-12-31",
        "source_url": "https://lims.bis.gov.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 302 (Part 1): 2008", "product_category": "Electrical Appliances", "testing_capability": "Electrical appliance safety and performance testing"},
            {"is_number": "IS 4151: 2020", "product_category": "Helmets", "testing_capability": "Helmets shock absorption drop testing, chin-strap dynamic retention"},
            {"is_number": "IS 1786: 2008", "product_category": "TMT Rebars", "testing_capability": "Tensile and mechanical testing"},
            {"is_number": "IS 14543: 2016", "product_category": "Packaged Water", "testing_capability": "Bacteriological and pesticide residue analysis"}
        ]
    },
    {
        "lab_code": "BIS-BLR-006",
        "name": "Bureau of Indian Standards Branch Laboratory Bengaluru",
        "address": "Peenya Industrial Area, 1st Stage, Tumkur Road, Bengaluru",
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "pincode": "560058",
        "latitude": 13.0298,
        "longitude": 77.5186,
        "contact_person": "Scientist-E & Head, BIS Branch Laboratory",
        "phone": "+91-80-28394955",
        "email": "bnbo@bis.gov.in",
        "lab_type": "BIS Branch Laboratory",
        "status": "Recognized",
        "recognition_valid_until": "2030-12-31",
        "source_url": "https://lims.bis.gov.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 302 (Part 1): 2008", "product_category": "Electrical Appliances", "testing_capability": "Electrical safety and insulation resistance"},
            {"is_number": "IS 14543: 2016", "product_category": "Packaged Water", "testing_capability": "Packaged drinking water comprehensive quality testing"},
            {"is_number": "IS 4985: 2021", "product_category": "uPVC Pipes", "testing_capability": "Hydrostatic pressure, impact strength at 0°C, toxic element extraction"}
        ]
    },
    {
        "lab_code": "BIS-GHY-007",
        "name": "Bureau of Indian Standards Branch Laboratory Guwahati",
        "address": "NEDFi House, 4th Floor, G.S. Road, Dispur, Guwahati",
        "city": "Guwahati",
        "district": "Kamrup Metropolitan",
        "state": "Assam",
        "pincode": "781006",
        "latitude": 26.1445,
        "longitude": 91.7901,
        "contact_person": "Scientist-E & Head, BIS Guwahati",
        "phone": "+91-361-2232970",
        "email": "ghbo@bis.gov.in",
        "lab_type": "BIS Branch Laboratory",
        "status": "Recognized",
        "recognition_valid_until": "2030-12-31",
        "source_url": "https://lims.bis.gov.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 14543: 2016", "product_category": "Packaged Water", "testing_capability": "Physicochemical and microbial pathogens testing"},
            {"is_number": "IS 269: 2015", "product_category": "Cement", "testing_capability": "Cement physical and chemical testing"},
            {"is_number": "IS 1786: 2008", "product_category": "TMT Rebars", "testing_capability": "Rebar tensile and bend testing"}
        ]
    },
    {
        "lab_code": "BIS-PAT-008",
        "name": "Bureau of Indian Standards Branch Laboratory Patna",
        "address": "Patliputra Industrial Area, Patna",
        "city": "Patna",
        "district": "Patna",
        "state": "Bihar",
        "pincode": "800013",
        "latitude": 25.6207,
        "longitude": 85.0975,
        "contact_person": "Scientist-E & Head, BIS Patna",
        "phone": "+91-612-2262305",
        "email": "ptbo@bis.gov.in",
        "lab_type": "BIS Branch Laboratory",
        "status": "Recognized",
        "recognition_valid_until": "2030-12-31",
        "source_url": "https://lims.bis.gov.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 14543: 2016", "product_category": "Packaged Water", "testing_capability": "Complete water testing"},
            {"is_number": "IS 1786: 2008", "product_category": "TMT Rebars", "testing_capability": "Mechanical testing of steel"}
        ]
    },
    {
        "lab_code": "BIS-AHM-009",
        "name": "Bureau of Indian Standards Branch Laboratory Ahmedabad",
        "address": "Pushpak, 3rd Floor, Khanpur, Ahmedabad",
        "city": "Ahmedabad",
        "district": "Ahmedabad",
        "state": "Gujarat",
        "pincode": "380001",
        "latitude": 23.0284,
        "longitude": 72.5800,
        "contact_person": "Scientist-E & Head, BIS Ahmedabad",
        "phone": "+91-79-25601297",
        "email": "ahbo@bis.gov.in",
        "lab_type": "BIS Branch Laboratory",
        "status": "Recognized",
        "recognition_valid_until": "2030-12-31",
        "source_url": "https://lims.bis.gov.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 252: 2013", "product_category": "Chemicals", "testing_capability": "Caustic soda chemical assay and purity"},
            {"is_number": "IS 15622: 2017", "product_category": "Ceramic Tiles", "testing_capability": "Water absorption, modulus of rupture, chemical resistance"},
            {"is_number": "IS 14543: 2016", "product_category": "Packaged Water", "testing_capability": "Water testing parameters"}
        ]
    },
    {
        "lab_code": "BIS-HYD-010",
        "name": "Bureau of Indian Standards Branch Laboratory Hyderabad",
        "address": "F-9/A, Industrial Development Area, Nacharam, Hyderabad",
        "city": "Hyderabad",
        "district": "Medchal-Malkajgiri",
        "state": "Telangana",
        "pincode": "500076",
        "latitude": 17.4329,
        "longitude": 78.5638,
        "contact_person": "Scientist-E & Head, BIS Hyderabad",
        "phone": "+91-40-27170823",
        "email": "hybo@bis.gov.in",
        "lab_type": "BIS Branch Laboratory",
        "status": "Recognized",
        "recognition_valid_until": "2030-12-31",
        "source_url": "https://lims.bis.gov.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 302 (Part 1): 2008", "product_category": "Electrical Appliances", "testing_capability": "Appliance electrical safety"},
            {"is_number": "IS 4985: 2021", "product_category": "uPVC Pipes", "testing_capability": "PVC pipe burst testing"},
            {"is_number": "IS 14543: 2016", "product_category": "Packaged Water", "testing_capability": "Water potability and microbiological testing"}
        ]
    },

    # --- National Autonomous Government Institutes & Laboratories ---
    {
        "lab_code": "CPRI-BLR-011",
        "name": "Central Power Research Institute (CPRI) - Bengaluru Main Campus",
        "address": "Prof. Sir C.V. Raman Road, Sadashivanagar, Bengaluru",
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "pincode": "560080",
        "latitude": 13.0142,
        "longitude": 77.5756,
        "contact_person": "Director General / Joint Director (Testing)",
        "phone": "+91-80-22072222",
        "email": "director@cpri.in",
        "lab_type": "Government Autonomous Research Institute",
        "status": "Recognized",
        "recognition_valid_until": "2032-12-31",
        "source_url": "https://cpri.res.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 1180 (Part 1): 2014", "product_category": "Distribution Transformers", "testing_capability": "Full short circuit dynamic withstand test, lightning impulse, temperature rise"},
            {"is_number": "IS 7098 (Part 1): 1988", "product_category": "XLPE Power Cables", "testing_capability": "Partial discharge, high voltage withstand, thermal aging"},
            {"is_number": "IS 7098 (Part 2): 2011", "product_category": "Medium Voltage Cables", "testing_capability": "High voltage dielectric testing up to 132 kV, water treeing"},
            {"is_number": "IS/IEC 60898 (Part 1): 2002", "product_category": "Miniature Circuit Breakers (MCB)", "testing_capability": "Short circuit breaking capacity up to 25 kA, tripping characteristics"},
            {"is_number": "IS/IEC 61008 (Part 1): 2014", "product_category": "RCCB Residual Current Devices", "testing_capability": "Residual operating current, breaking time, short-circuit withstand"},
            {"is_number": "IS 1293: 2019", "product_category": "Plugs and Sockets", "testing_capability": "Endurance test under electrical load, breaking capacity, withdrawal force"},
            {"is_number": "IS 16444 (Part 1): 2015", "product_category": "Smart Energy Meters", "testing_capability": "Class 1 and 2 accuracy, tamper immunity, DLMS/COSEM communication protocol"},
            {"is_number": "IS 17017 (Part 1): 2018", "product_category": "EV Charging Systems", "testing_capability": "EVSE electrical safety, insulation monitoring, short circuit protection"},
            {"is_number": "IS 17017 (Part 2/Sec 1): 2020", "product_category": "EV Connectors", "testing_capability": "EV coupler mating endurance 10,000 cycles, ingress protection IP55, vehicle drive-over test"}
        ]
    },
    {
        "lab_code": "CPRI-BPL-012",
        "name": "Central Power Research Institute (CPRI) - Bhopal Switchgear Testing Station",
        "address": "Govindpura, Bhopal",
        "city": "Bhopal",
        "district": "Bhopal",
        "state": "Madhya Pradesh",
        "pincode": "462023",
        "latitude": 23.2599,
        "longitude": 77.4646,
        "contact_person": "Additional Director & Head, CPRI Bhopal",
        "phone": "+91-755-2586619",
        "email": "cpribpl@cpri.in",
        "lab_type": "Government Autonomous Research Institute",
        "status": "Recognized",
        "recognition_valid_until": "2032-12-31",
        "source_url": "https://cpri.res.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 1180 (Part 1): 2014", "product_category": "Transformers", "testing_capability": "High power short circuit testing, sound level, loss measurement"},
            {"is_number": "IS/IEC 60898 (Part 1): 2002", "product_category": "Circuit Breakers", "testing_capability": "Short circuit breaking and making capacity"}
        ]
    },
    {
        "lab_code": "CPRI-NOI-013",
        "name": "Central Power Research Institute (CPRI) - Noida Thermal Research Centre",
        "address": "A-1, Institutional Area, Sector 62, Noida",
        "city": "Noida",
        "district": "Gautam Buddha Nagar",
        "state": "Uttar Pradesh",
        "pincode": "201309",
        "latitude": 28.6270,
        "longitude": 77.3725,
        "contact_person": "Joint Director & Head, CPRI Noida",
        "phone": "+91-120-2402284",
        "email": "cprinoida@cpri.in",
        "lab_type": "Government Autonomous Research Institute",
        "status": "Recognized",
        "recognition_valid_until": "2032-12-31",
        "source_url": "https://cpri.res.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 694: 2010", "product_category": "Cables and Wires", "testing_capability": "Fire survival and flame retardancy tests"},
            {"is_number": "IS 7098 (Part 1): 1988", "product_category": "Power Cables", "testing_capability": "Electrical dielectric withstand and insulation thermal aging"}
        ]
    },
    {
        "lab_code": "ERDA-VAD-014",
        "name": "Electrical Research and Development Association (ERDA) - Vadodara",
        "address": "ERDA Road, GIDC, Makarpura, Vadodara",
        "city": "Vadodara",
        "district": "Vadodara",
        "state": "Gujarat",
        "pincode": "390010",
        "latitude": 22.2536,
        "longitude": 73.1979,
        "contact_person": "Director & Chief Operating Officer, ERDA",
        "phone": "+91-265-3043128",
        "email": "erda@erda.org",
        "lab_type": "Government Autonomous Research Institute",
        "status": "Recognized",
        "recognition_valid_until": "2031-08-31",
        "source_url": "https://www.erda.org/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 1180 (Part 1): 2014", "product_category": "Distribution Transformers", "testing_capability": "Full type tests, temperature rise, impulse test, acoustic sound level, oil breakdown"},
            {"is_number": "IS 12615: 2018", "product_category": "Electric Motors", "testing_capability": "IE2, IE3, IE4 energy efficiency rating, dynamometer load testing"},
            {"is_number": "IS 694: 2010", "product_category": "Cables", "testing_capability": "Complete physical, electrical, and flammability testing"},
            {"is_number": "IS 7098 (Part 1): 1988", "product_category": "XLPE Cables", "testing_capability": "High voltage and insulation resistance testing"},
            {"is_number": "IS 16221 (Part 2): 2015", "product_category": "Solar Inverters", "testing_capability": "Solar inverter efficiency, anti-islanding, harmonics and EMC"},
            {"is_number": "IS 16444 (Part 1): 2015", "product_category": "Smart Meters", "testing_capability": "Meter accuracy, magnetic tamper test, climatic chamber tests"}
        ]
    },
    {
        "lab_code": "ERDA-GUR-015",
        "name": "Electrical Research and Development Association (ERDA) - Gurugram",
        "address": "Plot No. 57, Sector 7, IMT Manesar, Gurugram",
        "city": "Gurugram",
        "district": "Gurugram",
        "state": "Haryana",
        "pincode": "122050",
        "latitude": 28.3610,
        "longitude": 76.9280,
        "contact_person": "Head of Northern Region Laboratory, ERDA",
        "phone": "+91-124-4286700",
        "email": "erdanorth@erda.org",
        "lab_type": "Government Autonomous Research Institute",
        "status": "Recognized",
        "recognition_valid_until": "2031-08-31",
        "source_url": "https://www.erda.org/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 17017 (Part 1): 2018", "product_category": "EV Chargers", "testing_capability": "AC & DC fast charger safety and performance testing"},
            {"is_number": "IS 15885 (Part 2/Sec 13): 2012", "product_category": "LED Drivers", "testing_capability": "Surge immunity, harmonic distortion, thermal testing"},
            {"is_number": "IS 16102 (Part 1): 2012", "product_category": "LED Lamps", "testing_capability": "Electrical safety and insulation resistance"}
        ]
    },
    {
        "lab_code": "NISE-GUR-016",
        "name": "National Institute of Solar Energy (NISE)",
        "address": "Gwal Pahari, Gurugram-Faridabad Road, Gurugram",
        "city": "Gurugram",
        "district": "Gurugram",
        "state": "Haryana",
        "pincode": "122003",
        "latitude": 28.4239,
        "longitude": 77.1517,
        "contact_person": "Director General & Head Solar Testing Centre",
        "phone": "+91-124-2579207",
        "email": "director.nise@gov.in",
        "lab_type": "Government Autonomous Research Institute",
        "status": "Recognized",
        "recognition_valid_until": "2032-06-30",
        "source_url": "https://nise.res.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 14286: 2010", "product_category": "Solar PV Modules", "testing_capability": "Class AAA solar simulator flash testing, UV preconditioning, damp heat (85°C/85% RH 1000h), mechanical load (5400 Pa), hail impact (25mm ice ball at 23 m/s)"},
            {"is_number": "IS/IEC 61730 (Part 1): 2004", "product_category": "Solar PV Modules", "testing_capability": "Construction safety, creepage distance, dielectric withstand"},
            {"is_number": "IS/IEC 61730 (Part 2): 2004", "product_category": "Solar PV Modules", "testing_capability": "Impulse voltage test, fire safety test, wet leakage current test"},
            {"is_number": "IS 16221 (Part 2): 2015", "product_category": "Solar Inverters", "testing_capability": "Inverter conversion efficiency, temperature rise, islanding protection"}
        ]
    },
    {
        "lab_code": "NTH-KOL-017",
        "name": "National Test House (ER) - Alipore, Kolkata",
        "address": "11/1 Judges Court Road, Alipore, Kolkata",
        "city": "Kolkata",
        "district": "Kolkata",
        "state": "West Bengal",
        "pincode": "700027",
        "latitude": 22.5298,
        "longitude": 88.3312,
        "contact_person": "Director, National Test House (Eastern Region)",
        "phone": "+91-33-24791580",
        "email": "nth-alipore@nic.in",
        "lab_type": "Government Autonomous Research Institute",
        "status": "Recognized",
        "recognition_valid_until": "2030-10-31",
        "source_url": "https://nth.gov.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 1786: 2008", "product_category": "TMT Steel Bars", "testing_capability": "Complete chemical composition by optical emission spectrometer (OES), tensile testing, bend test"},
            {"is_number": "IS 2062: 2011", "product_category": "Structural Steel", "testing_capability": "Tensile stress, impact toughness, chemical analysis of carbon and manganese"},
            {"is_number": "IS 269: 2015", "product_category": "Cement", "testing_capability": "Full chemical and physical cement analysis"},
            {"is_number": "IS 15298 (Part 2): 2016", "product_category": "Safety Footwear", "testing_capability": "Toe cap impact resistance, sole flex cracking, water penetration"},
            {"is_number": "IS 14543: 2016", "product_category": "Packaged Water", "testing_capability": "Pesticide residues GC-MS/MS, toxic metals ICP-MS, microbiological assays"}
        ]
    },
    {
        "lab_code": "NTH-MUM-018",
        "name": "National Test House (WR) - Mumbai",
        "address": "Plot No. F-10, MIDC Road, Marol, Andheri (East), Mumbai",
        "city": "Mumbai",
        "district": "Mumbai Suburban",
        "state": "Maharashtra",
        "pincode": "400093",
        "latitude": 19.1223,
        "longitude": 72.8756,
        "contact_person": "Director, National Test House (Western Region)",
        "phone": "+91-22-28325148",
        "email": "nth-mumbai@nic.in",
        "lab_type": "Government Autonomous Research Institute",
        "status": "Recognized",
        "recognition_valid_until": "2030-10-31",
        "source_url": "https://nth.gov.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 252: 2013", "product_category": "Caustic Soda", "testing_capability": "Pure and technical grade caustic soda chemical analysis"},
            {"is_number": "IS 517: 2020", "product_category": "Methanol", "testing_capability": "Methanol distillation range, purity and acidity tests"},
            {"is_number": "IS 302 (Part 1): 2008", "product_category": "Electrical Appliances", "testing_capability": "Household appliance electrical safety and earth continuity"},
            {"is_number": "IS 694: 2010", "product_category": "Cables", "testing_capability": "Cable conductor resistance, insulation tensile strength and elongation"}
        ]
    },
    {
        "lab_code": "NTH-CHE-019",
        "name": "National Test House (SR) - Chennai",
        "address": "Tharamani, CSIR Road, Taramani, Chennai",
        "city": "Chennai",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "pincode": "600113",
        "latitude": 12.9875,
        "longitude": 80.2450,
        "contact_person": "Director, National Test House (Southern Region)",
        "phone": "+91-44-22541356",
        "email": "nth-chennai@nic.in",
        "lab_type": "Government Autonomous Research Institute",
        "status": "Recognized",
        "recognition_valid_until": "2030-10-31",
        "source_url": "https://nth.gov.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 269: 2015", "product_category": "Cement", "testing_capability": "Compressive strength, setting time, soundess"},
            {"is_number": "IS 15622: 2017", "product_category": "Ceramic Tiles", "testing_capability": "Water absorption, MOR, scratch hardness, deep abrasion"},
            {"is_number": "IS 2553 (Part 1): 2018", "product_category": "Safety Glass", "testing_capability": "Toughened glass fragmentation test, 227g steel ball impact test"}
        ]
    },
    {
        "lab_code": "NTH-GHA-020",
        "name": "National Test House (NR) - Ghaziabad",
        "address": "Kamla Nehru Nagar, Ghaziabad",
        "city": "Ghaziabad",
        "district": "Ghaziabad",
        "state": "Uttar Pradesh",
        "pincode": "201002",
        "latitude": 28.6750,
        "longitude": 77.4410,
        "contact_person": "Director, National Test House (Northern Region)",
        "phone": "+91-120-2783002",
        "email": "nth-ghaziabad@nic.in",
        "lab_type": "Government Autonomous Research Institute",
        "status": "Recognized",
        "recognition_valid_until": "2030-10-31",
        "source_url": "https://nth.gov.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 694: 2010", "product_category": "Cables", "testing_capability": "Conductor resistance, insulation resistance, flame propagation"},
            {"is_number": "IS 13252 (Part 1): 2010", "product_category": "IT Equipment", "testing_capability": "Safety of power adapters, computers, and visual display units"},
            {"is_number": "IS 14543: 2016", "product_category": "Packaged Water", "testing_capability": "Physicochemical and pesticide residue analysis"}
        ]
    },
    {
        "lab_code": "CIPET-CHE-021",
        "name": "Central Institute of Petrochemicals Engineering & Technology (CIPET: IPT) - Chennai",
        "address": "TVK Industrial Estate, Guindy, Chennai",
        "city": "Chennai",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "pincode": "600032",
        "latitude": 13.0102,
        "longitude": 80.2036,
        "contact_person": "Principal Director & Head, CIPET Chennai",
        "phone": "+91-44-22254701",
        "email": "chennai@cipet.gov.in",
        "lab_type": "Government Autonomous Research Institute",
        "status": "Recognized",
        "recognition_valid_until": "2031-12-31",
        "source_url": "https://www.cipet.gov.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 4985: 2021", "product_category": "uPVC Pipes", "testing_capability": "Internal hydrostatic pressure at 20°C and 60°C, resistance to external blows at 0°C, toxic elements migration (lead, cadmium)"},
            {"is_number": "IS 4984: 2016", "product_category": "HDPE Pipes", "testing_capability": "Hydrostatic strength, oxidation induction time (OIT), carbon black content and dispersion, melt flow index"},
            {"is_number": "IS 6721: 2023", "product_category": "PVC Footwear", "testing_capability": "Tensile properties, hardness Shore A, split tear strength, flexing endurance"},
            {"is_number": "IS 10702: 2023", "product_category": "Rubber Footwear", "testing_capability": "Hawai chappal tensile strength, strap attachment force, abrasion loss"}
        ]
    },
    {
        "lab_code": "CIPET-AHM-022",
        "name": "Central Institute of Petrochemicals Engineering & Technology (CIPET: IPT) - Ahmedabad",
        "address": "Plot No. 630, Phase-IV, GIDC, Vatva, Ahmedabad",
        "city": "Ahmedabad",
        "district": "Ahmedabad",
        "state": "Gujarat",
        "pincode": "382445",
        "latitude": 22.9714,
        "longitude": 72.6369,
        "contact_person": "Director & Head, CIPET Ahmedabad",
        "phone": "+91-79-40103903",
        "email": "ahmedabad@cipet.gov.in",
        "lab_type": "Government Autonomous Research Institute",
        "status": "Recognized",
        "recognition_valid_until": "2031-12-31",
        "source_url": "https://www.cipet.gov.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 4985: 2021", "product_category": "uPVC Pipes", "testing_capability": "Hydrostatic pressure, impact, toxic metal extraction"},
            {"is_number": "IS 4984: 2016", "product_category": "HDPE Pipes", "testing_capability": "Carbon black, tensile strength, melt flow rate"},
            {"is_number": "IS 6721: 2023", "product_category": "PVC Footwear", "testing_capability": "Polymeric footwear material testing"}
        ]
    },
    {
        "lab_code": "CIPET-BBU-023",
        "name": "Central Institute of Petrochemicals Engineering & Technology (CIPET: IPT) - Bhubaneswar",
        "address": "B-25, Chandaka Industrial Area, KIIT Post, Patia, Bhubaneswar",
        "city": "Bhubaneswar",
        "district": "Khordha",
        "state": "Odisha",
        "pincode": "751024",
        "latitude": 20.3541,
        "longitude": 85.8194,
        "contact_person": "Director & Head, CIPET Bhubaneswar",
        "phone": "+91-674-2743462",
        "email": "bhubaneswar@cipet.gov.in",
        "lab_type": "Government Autonomous Research Institute",
        "status": "Recognized",
        "recognition_valid_until": "2031-12-31",
        "source_url": "https://www.cipet.gov.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 4985: 2021", "product_category": "uPVC Pipes", "testing_capability": "Complete plastic pipe testing"},
            {"is_number": "IS 4984: 2016", "product_category": "HDPE Pipes", "testing_capability": "HDPE pipe pressure and material testing"}
        ]
    },
    {
        "lab_code": "IPIRTI-BLR-024",
        "name": "Indian Plywood Industries Research and Training Institute (IPIRTI) - Bengaluru",
        "address": "Post Bag No. 2273, Tumkur Road, Yeshwanthpur, Bengaluru",
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "pincode": "560022",
        "latitude": 13.0232,
        "longitude": 77.5458,
        "contact_person": "Director & Head of Testing Division, IPIRTI",
        "phone": "+91-80-30534000",
        "email": "director@ipirti.gov.in",
        "lab_type": "Government Autonomous Research Institute",
        "status": "Recognized",
        "recognition_valid_until": "2032-12-31",
        "source_url": "https://ipirti.gov.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 710: 2010", "product_category": "Marine Plywood", "testing_capability": "72-hour boiling water test (BWP), adhesive bond shear strength, mycological test, moisture content, tensile strength"},
            {"is_number": "IS 303: 1989", "product_category": "General Purpose Plywood", "testing_capability": "MR and BWR grade glue adhesion, flexural modulus of elasticity, retention of modulus of rupture"},
            {"is_number": "IS 2202 (Part 1): 1999", "product_category": "Flush Door Shutters", "testing_capability": "End slam test (1000 slams), edge loading test, shock resistance with 50kg sandbag, immersion test in water"}
        ]
    },
    {
        "lab_code": "ARAI-PUN-025",
        "name": "Automotive Research Association of India (ARAI) - Pune",
        "address": "Survey No. 102, Vetal Hill, Off Paud Road, Kothrud, Pune",
        "city": "Pune",
        "district": "Pune",
        "state": "Maharashtra",
        "pincode": "411038",
        "latitude": 18.5173,
        "longitude": 73.8152,
        "contact_person": "Director & Head Homologation & Safety Components, ARAI",
        "phone": "+91-20-30231111",
        "email": "director@araiindia.com",
        "lab_type": "Government Autonomous Research Institute",
        "status": "Recognized",
        "recognition_valid_until": "2032-12-31",
        "source_url": "https://www.araiindia.com/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 4151: 2020", "product_category": "Two-Wheeler Helmets", "testing_capability": "Shock absorption with tri-axial accelerometer, dynamic retention chinstrap test, peripheral vision test, visor light transmission and scratch resistance"},
            {"is_number": "IS 15633: 2005", "product_category": "Passenger Car Tyres", "testing_capability": "High-speed endurance drum test, bead unseating resistance, plunger breaking energy"},
            {"is_number": "IS 15636: 2012", "product_category": "Commercial Vehicle Tyres", "testing_capability": "Endurance testing under variable loads, tyre strength and tread wear"},
            {"is_number": "IS 2553 (Part 2): 2019", "product_category": "Automotive Safety Glass", "testing_capability": "Windscreen phantom headform impact test, 227g ball impact, secondary image separation, optical distortion"}
        ]
    },
    {
        "lab_code": "ICAT-MAN-026",
        "name": "International Centre for Automotive Technology (ICAT) - Manesar",
        "address": "Plot 26, Sector 3, HSIIDC, IMT Manesar, Gurugram",
        "city": "Gurugram",
        "district": "Gurugram",
        "state": "Haryana",
        "pincode": "122050",
        "latitude": 28.3547,
        "longitude": 76.9213,
        "contact_person": "Director & General Manager (Testing & Certification), ICAT",
        "phone": "+91-124-4586111",
        "email": "icat@icat.ac.in",
        "lab_type": "Government Autonomous Research Institute",
        "status": "Recognized",
        "recognition_valid_until": "2032-12-31",
        "source_url": "https://icat.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 4151: 2020", "product_category": "Protective Helmets", "testing_capability": "Full helmet safety and impact testing under temperature conditioning"},
            {"is_number": "IS 15633: 2005", "product_category": "Automotive Tyres", "testing_capability": "High-speed tyre endurance testing"},
            {"is_number": "IS 2553 (Part 2): 2019", "product_category": "Automotive Safety Glass", "testing_capability": "Laminated and toughened windscreen optical and impact testing"}
        ]
    },
    {
        "lab_code": "CIRT-PUN-027",
        "name": "Central Institute of Road Transport (CIRT) - Pune",
        "address": "Post Box No. 1897, Pune-Nashik Road, Bhosari, Pune",
        "city": "Pune",
        "district": "Pune",
        "state": "Maharashtra",
        "pincode": "411026",
        "latitude": 18.6298,
        "longitude": 73.8344,
        "contact_person": "Director & Head Component Testing, CIRT",
        "phone": "+91-20-67345300",
        "email": "director@cirtindia.com",
        "lab_type": "Government Autonomous Research Institute",
        "status": "Recognized",
        "recognition_valid_until": "2031-12-31",
        "source_url": "http://www.cirtindia.com/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 4151: 2020", "product_category": "Two-Wheeler Helmets", "testing_capability": "Protective helmet impact and retention testing"},
            {"is_number": "IS 2553 (Part 2): 2019", "product_category": "Safety Glass", "testing_capability": "Automotive safety glazing testing"}
        ]
    },
    {
        "lab_code": "SRI-DEL-028",
        "name": "Shriram Institute for Industrial Research - Delhi",
        "address": "19, University Road, Block A, Timarpur, Delhi",
        "city": "Delhi",
        "district": "North Delhi",
        "state": "Delhi",
        "pincode": "110007",
        "latitude": 28.6946,
        "longitude": 77.2144,
        "contact_person": "Director & Head Materials & Chemical Testing",
        "phone": "+91-11-27667267",
        "email": "sridlhi@shriraminstitute.org",
        "lab_type": "Government Autonomous Research Institute",
        "status": "Recognized",
        "recognition_valid_until": "2031-10-31",
        "source_url": "https://www.shriraminstitute.org/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 9873 (Part 1): 2019", "product_category": "Toys", "testing_capability": "Mechanical and physical safety of toys"},
            {"is_number": "IS 9873 (Part 2): 2017", "product_category": "Toys", "testing_capability": "Flammability of plush and costume toys"},
            {"is_number": "IS 9873 (Part 3): 2020", "product_category": "Toys", "testing_capability": "Toxic elements migration analysis by ICP-OES and ICP-MS"},
            {"is_number": "IS 15644: 2006", "product_category": "Electric Toys", "testing_capability": "Safety of electric toys, heating, laser radiation and EMC"},
            {"is_number": "IS 14543: 2016", "product_category": "Packaged Water", "testing_capability": "Comprehensive 50+ parameter water analysis including pesticide residues and heavy metals"},
            {"is_number": "IS 15298 (Part 2): 2016", "product_category": "Footwear", "testing_capability": "Toe cap impact resistance and chemical resistance of safety shoes"}
        ]
    },
    {
        "lab_code": "CFTRI-MYS-029",
        "name": "Central Food Technological Research Institute (CSIR-CFTRI) - Mysuru",
        "address": "Cheluvamba Mansion, Opp. Railway Station, Mysuru",
        "city": "Mysuru",
        "district": "Mysuru",
        "state": "Karnataka",
        "pincode": "570020",
        "latitude": 12.3168,
        "longitude": 76.6433,
        "contact_person": "Director & Head Food Safety & Analytical Quality Control Laboratory (FSAQCL)",
        "phone": "+91-821-2514940",
        "email": "director@cftri.res.in",
        "lab_type": "Government Autonomous Research Institute",
        "status": "Recognized",
        "recognition_valid_until": "2032-12-31",
        "source_url": "https://www.cftri.res.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 14543: 2016", "product_category": "Packaged Water", "testing_capability": "Reference laboratory for pesticide residue detection, heavy metals, volatile organic carbons, and microbial pathogen isolation"},
            {"is_number": "IS 13428: 2005", "product_category": "Mineral Water", "testing_capability": "Mineral analysis, isotopic purity, sterility"},
            {"is_number": "IS 14433: 2022", "product_category": "Infant Milk Food", "testing_capability": "Macronutrients, amino acid profiling, micronutrients, aflatoxin M1 detection"}
        ]
    },
    {
        "lab_code": "SAMEER-MUM-030",
        "name": "Society for Applied Microwave Electronics Engineering and Research (SAMEER) - Mumbai",
        "address": "IIT Campus, Hill Side, Powai, Mumbai",
        "city": "Mumbai",
        "district": "Mumbai Suburban",
        "state": "Maharashtra",
        "pincode": "400076",
        "latitude": 19.1334,
        "longitude": 72.9133,
        "contact_person": "Director General & Head EMI/EMC Division",
        "phone": "+91-22-25727100",
        "email": "director@sameer.gov.in",
        "lab_type": "Government Autonomous Research Institute",
        "status": "Recognized",
        "recognition_valid_until": "2032-12-31",
        "source_url": "https://www.sameer.gov.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 13252 (Part 1): 2010", "product_category": "IT Equipment", "testing_capability": "Electromagnetic radiation, radiated emission, immunity against electrostatic discharge (ESD)"},
            {"is_number": "IS 616: 2017", "product_category": "Audio/Video Equipment", "testing_capability": "EMC compliance and safety"}
        ]
    },
    {
        "lab_code": "SAMEER-CHE-031",
        "name": "SAMEER - Centre for Electromagnetics - Chennai",
        "address": "CIT Campus, 2nd Cross Road, Taramani, Chennai",
        "city": "Chennai",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "pincode": "600113",
        "latitude": 12.9868,
        "longitude": 80.2439,
        "contact_person": "Programme Director & Head CEM, SAMEER Chennai",
        "phone": "+91-44-22541817",
        "email": "directorcem@sameer.gov.in",
        "lab_type": "Government Autonomous Research Institute",
        "status": "Recognized",
        "recognition_valid_until": "2032-12-31",
        "source_url": "https://cem.sameer.gov.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 13252 (Part 1): 2010", "product_category": "IT Equipment", "testing_capability": "Conducted and radiated emissions in 10-meter semi-anechoic chamber"},
            {"is_number": "IS 16444 (Part 1): 2015", "product_category": "Smart Meters", "testing_capability": "Smart meter RF emissions and surge immunity testing"}
        ]
    },
    {
        "lab_code": "STQC-DEL-032",
        "name": "Electronics Regional Test Laboratory (ERTL North) - STQC Delhi",
        "address": "S-Block, Okhla Industrial Area, Phase-II, New Delhi",
        "city": "New Delhi",
        "district": "South East Delhi",
        "state": "Delhi",
        "pincode": "110020",
        "latitude": 28.5273,
        "longitude": 77.2721,
        "contact_person": "Senior Director & Head ERTL (North)",
        "phone": "+91-11-26386219",
        "email": "ertlnorth@stqc.nic.in",
        "lab_type": "Government Autonomous Research Institute",
        "status": "Recognized",
        "recognition_valid_until": "2032-12-31",
        "source_url": "https://www.stqc.gov.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 13252 (Part 1): 2010", "product_category": "IT Equipment", "testing_capability": "Complete MeitY CRS Scheme-II type approval testing for laptops, servers, visual display units, barcode scanners"},
            {"is_number": "IS 16333 (Part 3): 2022", "product_category": "Mobile Handsets", "testing_capability": "Indian language input/rendering verification for 22 scheduled languages"},
            {"is_number": "IS 16046 (Part 2): 2018", "product_category": "Lithium Batteries", "testing_capability": "Overcharge, short-circuit, thermal abuse, impact, crush and forced discharge tests"},
            {"is_number": "IS 16242 (Part 1): 2014", "product_category": "UPS", "testing_capability": "UPS electrical safety, acoustic noise, efficiency"}
        ]
    },

    # --- Leading Accredited Private Testing Laboratories ---
    {
        "lab_code": "TUV-BLR-033",
        "name": "TUV Rheinland (India) Pvt. Ltd. - Bengaluru Main Laboratory",
        "address": "27/B, 2nd Cross Road, Electronic City Phase 1, Bengaluru",
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "pincode": "560100",
        "latitude": 12.8452,
        "longitude": 77.6603,
        "contact_person": "Vice President & Head of Testing Laboratories",
        "phone": "+91-80-46498000",
        "email": "info-ind@tuv.com",
        "lab_type": "Recognized Commercial Laboratory",
        "status": "Recognized",
        "recognition_valid_until": "2031-06-30",
        "source_url": "https://www.tuv.com/india/en/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 13252 (Part 1): 2010", "product_category": "IT Equipment", "testing_capability": "Complete CRS safety evaluation, creepage distance, electric shock protection"},
            {"is_number": "IS 616: 2017", "product_category": "Audio/Video", "testing_capability": "Smart TV, soundbar and amplifier safety testing"},
            {"is_number": "IS 16046 (Part 2): 2018", "product_category": "Lithium Batteries", "testing_capability": "Full UN 38.3 and IS 16046 part 2 battery safety test sequence"},
            {"is_number": "IS 14286: 2010", "product_category": "Solar PV Modules", "testing_capability": "Full PV module qualification in solar simulator and climate chambers"},
            {"is_number": "IS/IEC 61730 (Part 2): 2004", "product_category": "Solar PV Modules", "testing_capability": "PV module fire safety, reverse current overload, wet insulation resistance"},
            {"is_number": "IS 15885 (Part 2/Sec 13): 2012", "product_category": "LED Drivers", "testing_capability": "Electrical safety, thermal cycling, and fault condition testing"},
            {"is_number": "IS 16102 (Part 1): 2012", "product_category": "LED Lamps", "testing_capability": "LED bulb safety, cap temperature rise, insulation resistance"},
            {"is_number": "IS 302 (Part 1): 2008", "product_category": "Household Appliances", "testing_capability": "Electrical safety testing for domestic appliances"}
        ]
    },
    {
        "lab_code": "TUVSUD-GUR-034",
        "name": "TUV SUD South Asia Pvt. Ltd. - Gurugram Laboratory",
        "address": "Plot No. 373, Udyog Vihar Phase 2, Gurugram",
        "city": "Gurugram",
        "district": "Gurugram",
        "state": "Haryana",
        "pincode": "122016",
        "latitude": 28.5028,
        "longitude": 77.0815,
        "contact_person": "Senior Vice President & Head Testing Services",
        "phone": "+91-124-6199699",
        "email": "info.in@tuvsud.com",
        "lab_type": "Recognized Commercial Laboratory",
        "status": "Recognized",
        "recognition_valid_until": "2031-09-30",
        "source_url": "https://www.tuvsud.com/en-in",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 9873 (Part 1): 2019", "product_category": "Toys", "testing_capability": "Mechanical and physical safety tests for toys and children's products"},
            {"is_number": "IS 9873 (Part 2): 2017", "product_category": "Toys", "testing_capability": "Flammability testing in standardized burning chamber"},
            {"is_number": "IS 9873 (Part 3): 2020", "product_category": "Toys", "testing_capability": "Migration of toxic heavy elements by ICP-MS"},
            {"is_number": "IS 15644: 2006", "product_category": "Electric Toys", "testing_capability": "Electric toys safety and laser radiation verification"},
            {"is_number": "IS 15298 (Part 2): 2016", "product_category": "Safety Footwear", "testing_capability": "Toe cap impact, anti-static test, slip resistance on ceramic tile and steel floor"},
            {"is_number": "IS 13252 (Part 1): 2010", "product_category": "IT Equipment", "testing_capability": "Safety of IT and office equipment under MeitY CRS"}
        ]
    },
    {
        "lab_code": "UL-BLR-035",
        "name": "UL India Pvt. Ltd. - Bengaluru Testing Facility",
        "address": "Laboratory Building, Kalyani Platina, Campus 1, 3rd Floor, EPIP Zone, Whitefield, Bengaluru",
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "pincode": "560066",
        "latitude": 12.9815,
        "longitude": 77.7281,
        "contact_person": "Managing Director & Head of Laboratory",
        "phone": "+91-80-41384400",
        "email": "customercare.in@ul.com",
        "lab_type": "Recognized Commercial Laboratory",
        "status": "Recognized",
        "recognition_valid_until": "2031-11-30",
        "source_url": "https://india.ul.com/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 13252 (Part 1): 2010", "product_category": "IT Equipment", "testing_capability": "Full IT safety testing under CRS Scheme-II for computers, servers, printers, scanners"},
            {"is_number": "IS 16046 (Part 2): 2018", "product_category": "Lithium Batteries", "testing_capability": "Lithium ion cells and battery packs safety test, battery explosion chamber testing"},
            {"is_number": "IS 14286: 2010", "product_category": "Solar PV", "testing_capability": "Design qualification and environmental testing of solar PV modules"},
            {"is_number": "IS 16221 (Part 2): 2015", "product_category": "Solar Inverters", "testing_capability": "Solar power inverter safety and grid synchronization"},
            {"is_number": "IS 17017 (Part 1): 2018", "product_category": "EV Charging", "testing_capability": "EV charging station safety and protective earthing testing"}
        ]
    },
    {
        "lab_code": "INTERTEK-GUR-036",
        "name": "Intertek India Pvt. Ltd. - Gurugram Testing Centre",
        "address": "Plot No. 290, Udyog Vihar Phase 2, Gurugram",
        "city": "Gurugram",
        "district": "Gurugram",
        "state": "Haryana",
        "pincode": "122016",
        "latitude": 28.5042,
        "longitude": 77.0834,
        "contact_person": "General Manager & Head Electrical & Hardlines Testing",
        "phone": "+91-124-4503400",
        "email": "delhi.lab@intertek.com",
        "lab_type": "Recognized Commercial Laboratory",
        "status": "Recognized",
        "recognition_valid_until": "2031-07-31",
        "source_url": "https://www.intertek.com/india/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 9873 (Part 1): 2019", "product_category": "Toys", "testing_capability": "Mechanical and physical properties of toys"},
            {"is_number": "IS 9873 (Part 3): 2020", "product_category": "Toys", "testing_capability": "Toxic elements migration test by ICP-MS"},
            {"is_number": "IS 15644: 2006", "product_category": "Electric Toys", "testing_capability": "Electric toys safety"},
            {"is_number": "IS 302 (Part 1): 2008", "product_category": "Household Appliances", "testing_capability": "Safety of household appliances including irons, heaters, and geysers"},
            {"is_number": "IS 15885 (Part 2/Sec 13): 2012", "product_category": "LED Drivers", "testing_capability": "LED controlgear safety and reliability testing"}
        ]
    },
    {
        "lab_code": "SGS-GUR-037",
        "name": "SGS India Pvt. Ltd. - Gurugram Laboratory",
        "address": "250, Udyog Vihar Phase IV, Gurugram",
        "city": "Gurugram",
        "district": "Gurugram",
        "state": "Haryana",
        "pincode": "122015",
        "latitude": 28.4985,
        "longitude": 77.0860,
        "contact_person": "Business Director - Consumer and Retail Services",
        "phone": "+91-124-6060070",
        "email": "sgs.india@sgs.com",
        "lab_type": "Recognized Commercial Laboratory",
        "status": "Recognized",
        "recognition_valid_until": "2031-05-31",
        "source_url": "https://www.sgsgroup.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 9873 (Part 1): 2019", "product_category": "Toys", "testing_capability": "Comprehensive toy safety testing"},
            {"is_number": "IS 9873 (Part 3): 2020", "product_category": "Toys", "testing_capability": "Heavy metals migration analysis"},
            {"is_number": "IS 15298 (Part 2): 2016", "product_category": "Footwear", "testing_capability": "Industrial safety footwear toe cap and puncture resistance"},
            {"is_number": "IS 14543: 2016", "product_category": "Packaged Water", "testing_capability": "Water chemical and microbiology testing"}
        ]
    },
    {
        "lab_code": "BV-NOI-038",
        "name": "Bureau Veritas Consumer Products Services India - Noida",
        "address": "C-19, Sector 7, Noida",
        "city": "Noida",
        "district": "Gautam Buddha Nagar",
        "state": "Uttar Pradesh",
        "pincode": "201301",
        "latitude": 28.5992,
        "longitude": 77.3195,
        "contact_person": "General Manager & Technical Director",
        "phone": "+91-120-4368200",
        "email": "bvinformation@bureauveritas.com",
        "lab_type": "Recognized Commercial Laboratory",
        "status": "Recognized",
        "recognition_valid_until": "2031-04-30",
        "source_url": "https://www.bureauveritas.co.in/",
        "is_fixture": False,
        "scopes": [
            {"is_number": "IS 13252 (Part 1): 2010", "product_category": "IT Equipment", "testing_capability": "IT and office electronics CRS Scheme-II testing"},
            {"is_number": "IS 616: 2017", "product_category": "Audio/Video", "testing_capability": "Televisions and consumer electronic equipment safety"},
            {"is_number": "IS 302 (Part 1): 2008", "product_category": "Household Appliances", "testing_capability": "Appliance electrical safety, creepage distance, electric strength"}
        ]
    }
]

# Write all files
with open(SEED_DIR / "schemes.json", "w", encoding="utf-8") as f:
    json.dump(SCHEMES, f, indent=2)

with open(SEED_DIR / "qcos.json", "w", encoding="utf-8") as f:
    json.dump(QCOS, f, indent=2)

with open(SEED_DIR / "laboratories.json", "w", encoding="utf-8") as f:
    json.dump(LABORATORIES, f, indent=2)

print("SUCCESS: Generated comprehensive datasets:")
print(f"  - Schemes: {len(SCHEMES)}")
print(f"  - Standards: {len(STANDARDS)}")
print(f"  - QCOs: {len(QCOS)}")
print(f"  - Laboratories: {len(LABORATORIES)}")
scopes_total = sum(len(l.get("scopes", [])) for l in LABORATORIES)
print(f"  - Total Testing Scopes: {scopes_total}")
