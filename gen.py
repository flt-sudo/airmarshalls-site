import re,os
OUT='docs'
css=open('services-modern.html').read()
css=css[css.index('<style>')+7:css.index('</style>')]
css+='''
  .row2{display:grid;grid-template-columns:1fr 1fr;gap:18px;align-items:start}
  .figrow{display:grid;grid-template-columns:150px 1fr;gap:16px;align-items:start;margin:14px 0}
  .figrow img{width:100%;height:auto;border-radius:4px;border:1px solid var(--rule)}
  .figrow.sm{grid-template-columns:100px 1fr}
  .quotes{list-style:none;padding:0;margin:8px 0 14px}
  .quotes li{font-weight:bold;margin:3px 0}
  .quotes li::before{content:"\\201C";color:var(--green);font-weight:bold;margin-right:4px}
  .molds{columns:2;padding-left:22px;margin:0}
  .molds li{font-weight:bold}
  .form label{display:block;font-size:14px;font-weight:bold;margin:10px 0 3px;color:#333}
  .form input,.form textarea,.form select{width:100%;padding:9px 10px;border:1px solid #b9c2cf;border-radius:4px;font:inherit;font-size:15px}
  .form textarea{min-height:110px}
  .form .btn{margin-top:12px;border:0;cursor:pointer;font:inherit}
  .form .note{font-size:13px;color:var(--grey);margin-top:8px}
  .award{color:var(--blue);font-weight:bold;text-decoration:underline}
  .qr{display:block;width:120px;margin:8px auto 0}
  .sealrow{display:flex;flex-wrap:wrap;gap:14px 24px;align-items:center;margin:14px 0}
  .sealrow img{height:56px;width:auto}
  .side .sealrow{justify-content:center;gap:10px 16px}
  .side .sealrow img{height:44px}
  @media (max-width:860px){.row2{grid-template-columns:1fr !important}.molds{columns:1}}
  @media (max-width:560px){
    body{font-size:16px;line-height:1.55}
    .wrap{padding:0 12px}
    .top{flex-direction:row;align-items:center;justify-content:space-between;gap:10px;padding:10px 0 8px}
    .brand img{height:64px}
    .contact{text-align:right}
    .contact .who{font-size:13px}
    .contact .mail{font-size:13px}
    .contact{flex:1;text-align:left;display:grid;grid-template-columns:1fr;gap:2px}
    .contact .who{font-size:13px;line-height:1.2}
    .btns{display:grid;grid-template-columns:1fr;gap:6px;margin-top:6px}
    .btn{padding:9px 8px;font-size:13px;text-align:center}
    .rated{font-size:12px;margin-top:4px;line-height:1.3}
    nav ul{display:grid;grid-template-columns:repeat(3,1fr);gap:0;overflow:visible}
    nav a{padding:10px 4px 10px 24px;font-size:14px;background-position:5px center;background-size:14px 14px;text-align:left;border-bottom-width:2px}
    .chips{grid-template-columns:1fr 1fr;gap:8px;padding-top:12px}
    .chip{padding:8px 10px;border-radius:5px}
    .chip b{font-size:15px}
    .chip small{font-size:12px;line-height:1.3}
    .chip.ir{gap:6px;align-items:flex-start}
    .chip.ir img{height:36px;margin-top:2px}
    .chip.ir b{font-size:14px}
    .tagline{font-size:14px;padding:10px 0 12px}
    .vids{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:10px;padding:0 0 14px;-webkit-overflow-scrolling:touch}
    .vids .video{flex:0 0 84%;scroll-snap-align:start}
    .layout{padding:14px 0 24px;gap:14px}
    .card{padding:16px 14px;border-radius:6px}
    .kicker{font-size:12px;gap:2px 10px;margin-bottom:4px}
    h1{font-size:26px;margin-bottom:10px}
    h2{font-size:20px}
    h3{font-size:15px;margin-top:18px}
    .lead{font-size:16px}
    .c{text-align:left !important}
    .banner{font-size:17px;text-align:left;margin:16px 0 2px}
    .photos{gap:6px}
    .figrow{grid-template-columns:90px 1fr;gap:10px}
    .figrow.sm{grid-template-columns:72px 1fr}
    .side .card{padding:16px 14px}
    .side .logo{width:120px}
    .creds{padding:16px 0 12px}
    .seals{gap:10px 16px}
    .seals img{height:40px}
    .seals img.sm{height:32px}
    .creds .nums{font-size:13px}
    .foot{font-size:12px;padding-bottom:96px}
    .callbar{display:grid;grid-template-columns:1fr 1fr;gap:8px;position:fixed;left:0;right:0;bottom:0;padding:8px 10px;background:#fff;border-top:1px solid var(--rule);z-index:9}
    .callbar .btn{text-align:center;font-size:14px;padding:10px 8px}
  }
'''
open(f'{OUT}/site.css','w').write(css)

def vid(id_,title): return f'<div class="video"><iframe src="https://www.youtube.com/embed/{id_}?rel=0" title="{title}" allowfullscreen loading="lazy"></iframe></div>'
TEL1='<a class="tel" style="text-decoration:none;color:inherit" href="tel:8558257770">855-825-7770</a>'
TEL2='<a class="tel red" style="text-decoration:none" href="tel:3182885363">318-288-5363</a>'
MAIL='<a href="mailto:federalassessor@aol.com">federalassessor@aol.com</a>'
FORM_JS='''<script>
function amSend(f){var b=[];for(var i=0;i<f.elements.length;i++){var e=f.elements[i];if(e.name&&e.value)b.push(e.name+": "+e.value);}
location.href="mailto:federalassessor@aol.com?subject="+encodeURIComponent("Website inquiry - "+(f.elements["Name"]?f.elements["Name"].value:""))+"&body="+encodeURIComponent(b.join("\\n"));return false;}
</script>'''
def form(fields):
    h='<form class="form" onsubmit="return amSend(this)">'
    for n in fields:
        if n=='Comments': h+=f'<label>{n} :</label><textarea name="{n}"></textarea>'
        elif n=='Type': h+=f'<label>{n} :</label><select name="{n}"><option></option><option>Residential</option><option>Commercial</option><option>Industrial</option><option>Other</option></select>'
        else:
            t="email" if n=="Email" else "tel" if n=="Phone" else "text"
            h+=f'<label>{n} :</label><input name="{n}" type="{t}">'
    h+='<button class="btn call" type="submit">Submit</button><div class="note">Sends from your own email app to federalassessor@aol.com.</div></form>'
    return h
CALLUS=f'''<div class="callus"><div class="t">Call Us Today!</div>Office: {TEL1}<br><span class="red b">Direct / Text: {TEL2}</span><br>Fax: 855-458-9469<br>email: {MAIL}</div>'''
TELL='<a class="tell" href="https://www.youtube.com/watch?v=1Jl-C5-OQ5M">Click here<br>And I will<br>Tell You More!</a>'
LADY='<img class="lady" src="img/Call_Lady.jpg" alt="Call us">'
LOGO='<img class="logo" src="img/logo_big.jpg" alt="Air Marshalls Environmental">'
LIC='<div class="licensed">LICENSED &amp; INSURED!</div>'
BLACKMOLD=vid('MgAu5U9Fxc4','Black Mold')
OSHA='<img src="img/seal_osha_epa_cdc.jpg" alt="OSHA, EPA, CDC" style="height:34px">'
GREENBIZ='<img src="img/seal_green_business.jpg" alt="Green Business member" style="height:60px">'
def figrow(img,alt,body,sm=False): return f'<div class="figrow{" sm" if sm else ""}"><img src="img/{img}" alt="{alt}"><div>{body}</div></div>'

def shell(slug,title,videos,main,side):
    nav=''.join(f'<li><a href="{s}.html"{" class=\"here\"" if s==slug else ""}>{t}</a></li>' for s,t in [('index','Home'),('services','Services'),('about','About Us'),('about_mold','About Mold'),('partner','Partners'),('contact','Contact Us')])
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} - Air Marshalls Environmental</title>
<meta name="description" content="Air Marshalls Environmental: licensed, insured, certified Indoor Air Quality consulting and sampling. Mold, asbestos, radon, methane, soil gas, LEED, meth. Office 855-825-7770.">
<link rel="canonical" href="https://www.airmarshallsenvironmental.org/{slug if slug!='index' else ''}{'.html' if slug!='index' else ''}">
<link rel="icon" href="img/favicon.png">
<link rel="stylesheet" href="site.css">
</head>
<body>
<div class="sky">
  <div class="wrap">
    <div class="top">
      <a class="brand" href="index.html"><img src="img/logo_big.jpg" alt="Air Marshalls Environmental - The Highest Quality Sampling"></a>
      <div class="contact">
        <div class="who">Federal Assessor</div>
        <div class="mail">{MAIL}</div>
        <div class="btns">
          <a class="btn call tel" href="tel:8558257770">Call 855-825-7770</a>
          <a class="btn text tel" href="tel:3182885363">Direct / Text 318-288-5363</a>
        </div>
        <div class="rated">We are <span class="red">A+ Five "5" Star</span> Rated! &nbsp;·&nbsp; Licensed and Insured</div>
      </div>
    </div>
  </div>
  <nav><div class="wrap"><ul>{nav}</ul></div></nav>
</div>

<div class="wrap">
  <div class="chips">
    <div class="chip"><b class="red">Asbestos</b><small>Non-Friable &amp; Friable Assessment Inspection Sampling.</small></div>
    <div class="chip"><b class="green">METH</b><small>Methamphetamine Air &amp; surface Sampling.</small></div>
    <div class="chip"><b class="green">LEED</b><small>Credit 3.2 Indoor Air Quality Test Sampling.</small></div>
    <div class="chip ir"><img src="img/Copy_of_IR_camera.jpg" alt="Infrared camera with Fusion Technology"><span><b class="green" style="font-size:16px">Free infrared inspections!</b><small>Call Us Now! &nbsp;Infrared Camera w/ Fusion Technology</small></span></div>
  </div>
  <p class="tagline"><span class="u">RADON</span>, Soil Gas, Industrial Indoor Air Quality Exposure Assessment Sampling.</p>
  <div class="vids">{''.join(videos)}</div>
</div>

<div class="wrap layout">
  <main class="card">
    <div class="kicker">
      <span><b>Text Us At:</b> <a class="tel" style="text-decoration:none;color:inherit" href="tel:3182885363">318-288-5363</a></span>
      <span><b>Industrial Hygiene / Machine Working Fluid</b> &nbsp;LICENSED CERTIFIED Indoor Air Quality CONSULTING.</span>
    </div>
{main}
  </main>
  <aside class="side"><div class="card">
{side}
  </div></aside>
</div>

<div class="creds">
  <div class="wrap">
    <h4>Licensed · Certified · Accredited</h4>
    <div class="seals">
      <img src="img/seal_namp.jpg" alt="Certified NAMP - National Association of Mold Professionals">
      <img src="img/seal_bbb.jpg" alt="BBB Accredited Business">
      <img src="img/seal_iicrc.jpg" alt="Institute of Inspection Cleaning and Restoration Certification">
      <img src="img/seal_servicemagic.jpg" alt="Service Magic Seal of Approval">
      <img src="img/2009_07_16_Pro_Home_Insp_Institute.jpg" alt="PHII Certified - Professional Home Inspection Institute">
      <img class="sm" src="img/seal_osha_epa_cdc.jpg" alt="OSHA, EPA, CDC">
      <img class="sm" src="img/seal_angies.jpg" alt="Angie's List">
      <img class="sm" src="img/seal_cards.jpg" alt="MasterCard, Visa, Discover, American Express accepted">
    </div>
    <div class="nums"><b>License # MAC 1247</b> &nbsp;·&nbsp; <b>NAMP Certified Member #1166</b> &nbsp;·&nbsp; Accredited independent laboratory services only &nbsp;·&nbsp; Written assessments within days</div>
  </div>
</div>
<div class="wrap foot">
  <span class="line">Air Marshalls Environmental Professionals &nbsp; <span class="red">Office: 855-825-7770 or Direct/Text: 318-288-5363</span></span>
  <span>&copy; 2010 Air Marshalls Environmental. All Rights Reserved. &nbsp;·&nbsp; Website Designed by Ricky R Calhoun &copy; 2022</span>
</div>
<div class="callbar">
  <a class="btn call" href="tel:8558257770">Call 855-825-7770</a>
  <a class="btn text" href="tel:3182885363">Text 318-288-5363</a>
</div>
{FORM_JS}
</body>
</html>'''

pages={}
# ================= HOME =================
main=f'''
    <h1>Welcome to Air Marshalls Environmental</h1>
    <p class="b" style="color:var(--blue);text-decoration:underline">Radon, Soil Gas, Asbestos, &amp; LEED Credit IAQ SAMPLING</p>
    <div class="row2">
      <div>
        <h3 style="margin-top:6px">Sampling...Why Sample?</h3>
        <p class="lead">Mold is alive and it's everywhere!</p>
        <p>Even though Mold and Indoor Air Quality issues are all round us the good news is the effects, growth and spread can be controlled. The only way to be sure that your Indoor Environment is free of Mold Fungus &amp; Contaminants is to have it Assessed Sampled and Inspected.</p>
        <p class="b">"We are <span class="red">A+ Five (5) Star</span> Rated!"</p>
        <p><a href="https://www.youtube.com/watch?v=1Jl-C5-OQ5M">Click here to View Our Mold Commercial</a></p>
      </div>
      {vid('or1ymqfUZwc','Mold and Fungus in your food - Dr Lonnie Meisel')}
    </div>
    <p style="margin-top:14px">One rule of thumb is when a structure's Indoor Air Quality Contaminant levels exceed the levels found outdoors, many serious Indoor Air Quality (IAQ) related structural, and health problems, are very possible. There are many valid reasons to sample and/or inspect your property for Mold. Mold growth is always possible and can begin at anytime, anywhere, whenever conditions that support mold growth are present. Mold growth is unrelated to how New, how Clean, or how well, you maintain your property. High humidity and/or any source causing damp or wet conditions in a property can lead to the growth of Mold. High humidity, wet and damp conditions, need to be located, identified quickly, and properly eliminated. These humid, wet, and/or damp Mold growth supporting conditions can be the result of a flood, roof leak, leaking pipes, missing insulation, or excessive moisture in a structure, even if there is no outwardly visible evidence of mold. Call us for a <b>Highest Quality Professional Indoor Air Quality &amp; LEED Credit 3.2 Sampling / Inspection / Assessment.</b></p>
    <p class="b c" style="color:var(--blue);text-decoration:underline">"Now is the perfect time for your peace of mind."</p>
    <p class="b c">National Association of Mold Professionals<br><span class="green">NAMP Certified Member #1166 &nbsp; License # MAC1247</span><br>Over 36 years of systematic problem solving training, teaching and experience!</p>
    <p class="b red">"A+ Five (5) Star Rated!" in Customer Satisfaction, Report Accuracy, Job Efficiency and Proficiency.</p>
    <p class="b c">** Legionella, &amp; Sewage Contamination Sampling **</p>
    <div class="row2">
      <div>
        <h3>What We Do for you?</h3>
        <p class="b" style="color:var(--blue)">LICENSED Indoor Air Quality Consulting - LEED &amp; MOLD - SAMPLING / ASSESSMENT</p>
        <p>Our complete walk through Assessment of your structure, will provide us with the opportunity to find problem areas that may require Air and/or Surface Sampling and/or thermal imaging to correctly and accurately pinpoint the location, type, and scope. Air and Surface Sampling are tools that allow us to positively identify both toxic and evasive Indoor Mold growth.</p>
      </div>
      <figure style="margin:0"><img src="img/residential_pic_2.jpg" alt="Thermal image: tested wet, high moisture reading" style="width:100%;border-radius:4px;border:1px solid var(--rule)"><figcaption style="font-size:13px;color:var(--grey)">Tested Wet, High Moisture Reading: hidden moisture found with infrared</figcaption></figure>
    </div>
    <p class="b c" style="color:var(--blue);margin-top:10px">WE PROVIDE WRITTEN MOLD ASSESSMENTS WITHIN DAYS<br>GIVING ATTENTION TO THE SMALLEST DETAIL IS OUR BUSINESS</p>
    <p>Our inspections, detailed report writing, assessments and evaluations are professional, prompt, and accurate.</p>
    <ul>
      <li class="b red">24/7 AIR ASSESSMENT SAMPLING EMERGENCY RESPONSE!</li>
      <li class="b">LICENSED - INSURED - CERTIFIED PROFESSIONALS &nbsp; MAC1247</li>
      <li class="b">QUALIFIED AND EXPERIENCED</li>
    </ul>
    <p class="b c" style="font-style:italic;color:var(--blue);margin-top:12px">"We work hard to be one of the best at what we do...for you!"</p>
    <p class="b">Call Us Today! office: {TEL1} or Direct / Text: {TEL2}</p>
    <ul class="quotes">
      <li>Assessment Evaluation &amp; Mold Control"</li>
      <li>We Provide Sampling Results &amp; Solutions"</li>
      <li>Written Assessments within days"</li>
      <li>Remediation Recommendations"</li>
    </ul>
    <div class="closing">
      <p class="b">Industrial Hygiene / Machine Working Fluid Indoor Air Quality Sampling</p>
      <p class="b" style="font-style:italic;color:var(--blue)">Air Marshalls Environmental Professional Licensed Certified IAQ Consultants</p>
      <p>{MAIL} &nbsp;·&nbsp; <a href="index.html">www.airmarshallsenvironmental.org</a></p>
      <p class="b red">Office: {TEL1} or Direct / Text: {TEL2}</p>
    </div>'''
side=f'''
    {LIC}
    <h3 style="margin:0 0 4px;font-size:16px">Request a call back</h3>
    {form(['Name','Address','Phone','Email','Best time to contact','Type','Comments'])}
    <p style="margin-top:14px;text-align:center"><a href="https://www.youtube.com/watch?v=1Jl-C5-OQ5M">Click here to View Our Commercial</a></p>
    {LADY}
    <p class="c" style="font-size:14px"><a href="https://www.youtube.com/watch?v=1Jl-C5-OQ5M">Click here and I will Talk to you!</a></p>
    {CALLUS}
    {BLACKMOLD}
    <div class="sealrow" style="margin-top:14px">{OSHA}{GREENBIZ}</div>'''
pages['index']=('Home',[vid('By1R3_OJHyA','2017 Air Marshalls'),vid('1UCt2Y21LX0','An Introduction to Asbestos - Louisiana DEQ'),vid('gciSp5X40t0','Air Marshalls Environmental')],main,side)

# ================= SERVICES =================
sm=open('services-modern.html').read()
smain=sm[sm.index('<h1>Services</h1>'):sm.index('  </main>')]
sside=sm[sm.index('<div class="licensed">'):sm.index('    </div>\n  </aside>')]
pages['services']=('Services',[vid('1Jl-C5-OQ5M','2017 Air Marshalls'),vid('_JqlIKHHrag','Indoor Air Pollution'),vid('1UCt2Y21LX0','Chinese Drywall')],'    '+smain,'    '+sside)

# ================= ABOUT =================
DOC_TXT='Air Marshalls Environmental offers licensed Certified Indoor Air Quality Consulting, Inspections, and Assessment reports that are produced in the proper format to provide our clients with the understanding and documentation needed to support an individual&#39;s insurance claim that can be filed with all insurance providers.'
main=f'''
    <h1>About Us - Licensed Certified Consulting</h1>
    <p class="lead">Air Marshalls Environmental licensed Consultants take great pride in delivering top shelf professional environmental and Indoor Air Quality consulting and sampling services. Which means that in the effort to demonstrate our appreciation for you having trusted us with the sampling/inspection of your residential and/or commercial - industrial property, we will go above and beyond the call of duty to satisfy our every client. Air Marshalls Environmental fully understands the possibility of Indoor Air Quality and Mold related health issues, from this we promise to verify our findings to serve and protect our every client.</p>
    <p class="b red">Office: {TEL1} or Direct/Text: {TEL2}</p>
    {figrow('Mold_Check.jpg','Mold Check','<h3 style="margin-top:0">Accurate Full Detailed Assessments Inspections and Reports</h3><p>Air Marshalls Environmental is dedicated to providing prompt detailed reports on <b class="green">LEED</b> (IAQ) Contaminant Sampling, Legionella, Chinese Drywall, <b class="red">Sewage Contamination</b>, Water Damage inspections and Microbial concerns for residences and commercial property. Along with your mold inspection our certified consultants can include remediation protocols, recommendations and water damage assessments.</p>',sm=True)}
    {figrow('2009_07_16_Pro_Home_Insp_Institute.jpg','PHII Certified','<h3 style="margin-top:0">Professional <span class="green">Indoor Air Quality</span> - Licensed Certified Consultation</h3><p>Air Marshalls Environmental consultants are willing to assist customers in identifying problems and offer suggestions in the following areas: restoration and remediation, water damage, <b><i>Grade "D" Compressed Air sampling</i></b>, and microbial damage. We promise to be honest, always seeking the best solution, and provide prompt service resulting in the highest Indoor Air Quality possible for our every client.</p>',sm=True)}
    {figrow('about_element29.jpg','Moisture meter reading','<h3 style="margin-top:0">Air &amp; Surface Sampling - Industrial Hygiene / Machine Working Fluid Indoor Air Quality Sampling</h3><p>Air Marshalls Environmental licensed certified consultants are well adversed in the proper methods used in <b><i>Grade "D" Compressed Air</i></b>, obtaining Industrial (MWF) Air and Surface Indoor Air Quality samples to accurately identify microbial types that can cause serious allergic responses and a range of health Issues.</p>',sm=True)}
    <h3><span class="green">GREEN - LEED Credit</span> Indoor Air Quality Test Sampling</h3>
    <p class="b red">Formaldehyde, Particulates as PM10, Total Volatile Organic Compounds (TVOCs), Carbon Monoxide (CO) and 4-Phenylcyclohexene (4-PCH).</p>
    {figrow('IR_Image_2.jpg','Thermal image of hidden moisture','<h3 style="margin-top:0">Visual Inspections</h3><p>Air Marshalls Environmental Indoor Air Quality - Mold licensed certified consultants will perform a detailed complete fact finding walk through of your property and document our findings.</p><p>Infrared Imaging: <i>Air Marshalls</i> <b>Licensed Certified consultants</b> can provide <b>Thermal Imaging</b> as part of our complete Mold and Moisture Inspection and Assessment Services as well as <b>Energy Loss</b> Inspection and Assessment Services.</p>')}
    <p class="b red" style="text-align:right">Office: {TEL1} or Direct/Text: {TEL2}</p>
    {figrow('Talking_to_the_customer.jpg','Consultant reviewing findings with a customer','<h3 style="margin-top:0">Documentation</h3><p>'+DOC_TXT+'</p>')}
    <div class="closing">
      <p class="b" style="font-style:italic;color:var(--blue);text-decoration:underline">Accredited Laboratory services Only!</p>
      <p class="b red">Office: {TEL1} &nbsp; Direct / Text: {TEL2}</p>
    </div>'''
side=f'''
    <div class="licensed">INSURED &amp; LICENSED</div>
    {LOGO}{TELL}{LADY}{CALLUS}
    {vid('1dkMK8Mbts8','Black Mold Exposure')}
    {BLACKMOLD}
    <div class="sealrow" style="margin-top:14px">{OSHA}</div>'''
pages['about']=('About Us',[vid('1Jl-C5-OQ5M','2017 Air Marshalls'),vid('1dkMK8Mbts8','Black Mold Exposure'),vid('_JqlIKHHrag','Indoor Air Pollution')],main,side)

# ================= ABOUT MOLD =================
main=f'''
    <h1>About IAQ (MOLD)</h1>
    <p class="b" style="text-decoration:underline">What you should know...</p>
    <p class="b red">"A+ Five (5) Star Rating!" in Value, Customer Satisfaction, Report Accuracy, Job Efficiency and Proficiency.</p>
    <p class="b" style="color:var(--blue);text-decoration:underline">Grade D or better Breathing Air Quality Compressed Air - Radon - Methane - Soil Gas - Sampling.</p>
    <p>When remembering the curse of "King Tut's" tomb. It was not a "curse;" but Mold that caused the treasure hunters and workers who spent weeks working inside the tomb to die. Their activity caused the mold to become airborne, thus it was inhaled. Some tomb workers died sooner than others. Mold related illnesses affect different people in different ways. Mycotoxins are the metabolic byproduct of Mold and can be toxic to humans and pets. These Mycotoxins can result in allergies, cold/flu like symptoms, nose bleeds, fatigue, diarrhea, headaches, sore throats, soreness of the body, dermatitis and a weak compromised immune system. When found in any structure, Mold is a very real problem!</p>
    <div class="row2" style="grid-template-columns:220px 1fr">
      <div>
        <h3 style="margin-top:0">Toxic Molds</h3>
        <ul class="molds" style="columns:1"><li>Stachybotrys</li><li>Aspergillus</li><li>Penicillium</li><li>Cladosporium</li><li>Alternaria</li><li>Chaetomium</li><li>Fusarium</li><li>Acremonium</li></ul>
      </div>
      <div class="photos" style="grid-template-columns:1fr 1fr">
        <figure><img src="img/Wood_Mold_Picture1.jpg" alt="Mold growth on wood"><figcaption>Mold on framing lumber</figcaption></figure>
        <figure><img src="img/about_mold_element27.jpg" alt="Black mold on a wall"><figcaption>Black mold on drywall</figcaption></figure>
        <figure class="wide"><img src="img/residential_pic_5.jpg" alt="Mold growth at a wall base"><figcaption>Mold growth at the base of a wall</figcaption></figure>
      </div>
    </div>
    <p style="margin-top:14px">Almost <u>ALL</u> Molds produce mycotoxins and/or secondary metabolites which produce very powerful mycotoxins that can cause a wide range of health issues: flu like symptoms, bloody nose, sinus problems, headaches, nasal congestion, runny nose, breathing difficulties, chronic fatigue, skin sores, sore throats, eye infections, blindness and even cancer.</p>
    <p>These types of molds, appear Green, Brown, and/or Black in color.</p>
    <p>If you have a musty pungent odor or if someone in your home or building is experiencing any of the above listed symptoms call your doctor immediately and call Air Marshalls Environmental Consultants for a systematic consultation and/or detailed sampling/inspection of your property's Indoor Air Quality.</p>
    <p class="b" style="color:var(--blue)">Air Marshalls Environmental Professionals Consultants<br><span style="color:#111">Office:</span> {TEL1} &nbsp; <span class="red">Direct / Text: {TEL2}</span></p>
    <div class="row2" style="grid-template-columns:1fr 260px">
      <div>
        <h2 style="margin-top:6px">Are New Homes Mold, <span class="red">Radon</span>, Methane, and Soil Gas Free?</h2>
        <p>Assuming that a "new" home is free of Mold, Radon, Methane and Soil Gases, is a common mistake made by many new home owners. It is very possible that Mold is present on/in the building materials used in the construction of your new home. Often we have seen the wood framing and/or outside wood walls, and plywood roof of hundreds of new homes, while under construction, exposed to all kinds of weather. We have seen unprotected building materials on the ground. When unprotected building materials are exposed to adverse moisture producing weather conditions that support Mold growth, such as rain, snow and high humidity, Mold is very likely to grow in those building materials. Mold (microbial growth) loves to live in today's modern <b>"WAS WOOD"</b> building materials known in the industry as Medium Density Fiberboard (MDF), materials such as laminate flooring, chip wafer board, and drywall. Microbial growth, Radon, Methane and Soil Gases can, but does not always, produce odors that are pungent, deep musty or bitter.</p>
      </div>
      <figure style="margin:0"><img src="img/Residental_11.jpg" alt="New residential home" style="width:100%;border-radius:4px;border:1px solid var(--rule)"><figcaption style="font-size:13px;color:var(--grey)">New construction is not automatically mold-free</figcaption></figure>
    </div>
    <p>For Example Aspergillus fumigatus (A. fumigatus) is not a strong pathogen but it is believed to cause infections in immunosuppressed individuals. One Mold property known as "Microbial Volatile Organic Compounds" (MVOC's) or "Mycotoxins" are produced as Mold feeds (grows) and can damage the human "common chemical sense" which is associated with the trigeminal nerve which senses pungency.</p>
    <p><b style="color:var(--blue);text-decoration:underline">Poor Indoor Air Quality due to Mold, VOC's and Formaldehyde "Off Gassing" related health problems:</b> itching skin, burning skin, crawling skin, allergies, cough, nose bleeds, fever, eye infections, nausea, vomiting, diarrhea, swelling of the mucous membranes, respiratory problems, pulmonary infection muscle aches, dilation of blood vessels, decreased attention span problems, headaches, disorientation, slowed reflexes, dizziness and/or light headedness just to name a few. If you, or someone you know is experiencing any of the above listed symptoms contact a doctor immediately and call <i><b>Air Marshalls Environmental Consultants</b></i> for a systematic detailed inspection of the property in question. <b class="red">License # MAC 1247</b></p>
    <div class="closing">
      <p class="b" style="color:var(--blue);text-decoration:underline">Grade D or better Breathing Air Quality Compressed Air - Radon - Methane - Soil Gas - Sampling.</p>
      <p><b>Office:</b> {TEL1} &nbsp; <b>Direct / Text:</b> {TEL2} &nbsp; <i><b style="text-decoration:underline">Licensed, Insured, and Certified Indoor Air Quality Consulting</b></i></p>
    </div>'''
side=f'''
    <div class="licensed">INSURED &amp; LICENSED<br><span style="color:#111;font-weight:normal;font-size:14px">License # MAC 1247</span></div>
    {LOGO}
    <a class="tell" href="about.html">Click here<br>To Learn<br>About Us!</a>
    {vid('hEsHdBSiN7w','Toxic Black Mold Syndrome')}
    <img class="irimg" src="img/about_mold_element72.jpg" alt="Thermal image of hidden moisture">
    {BLACKMOLD}
    <div class="sealrow" style="margin-top:14px">{OSHA}{GREENBIZ}</div>'''
pages['about_mold']=('About Mold',[vid('1Jl-C5-OQ5M','2017 Air Marshalls'),vid('hEsHdBSiN7w','Toxic Black Mold Syndrome'),vid('or1ymqfUZwc','Mold and Fungus in your food')],main,side)

# ================= PARTNERS =================
main=f'''
    <h1>Partners</h1>
    <div class="banner" style="margin-top:0">LICENSED &amp; INSURED!</div>
    <h2><span class="red">Asbestos</span>, Radon and Soil Gas Sampling</h2>
    <p><b><span class="red">Asbestos</span>, Radon and Soil Gas Sampling:</b> Air Marshalls Environmental Licensed Certified consultants are equipped and trained in the use of the latest Strategies &amp; technologies to provide accurate and complete Asbestos, Radon and Soil Gas Sampling, assessments and reports to our clients.</p>
    <h2><span class="green">Methamphetamine</span> Air &amp; surface Sampling.</h2>
    <p><b><span class="red">Methamphetamine Air and Surface Sampling</span>:</b> Air Marshalls Environmental Certified consultants are equipped and trained in the use of the latest technologies to provide accurate and complete Methamphetamine Sampling, assessments and reports to our clients.</p>
    <div class="sealrow">
      <img src="img/seal_bbb.jpg" alt="BBB Accredited Business">
      <img src="img/seal_iicrc.jpg" alt="IICRC">
      <img src="img/seal_servicemagic.jpg" alt="Service Magic Seal of Approval">
      <img src="img/seal_namp.jpg" alt="Certified NAMP">
      {OSHA}
    </div>
    <p class="b c">Air Marshalls Environmental Professional Consultants<br><span style="font-weight:normal">LICENSED CERTIFIED Indoor Air Quality Assessment / Consulting.</span></p>
    <h3>Asbestos Assessments</h3>
    <p>Air Marshalls Environmental Licensed consultants are equipped and trained in the use of the latest technologies to provide accurate and complete Indoor Air Quality, Mold Sampling, assessments and reports to our clients.</p>
    <div class="row2" style="grid-template-columns:1fr 320px">
      <div>
        <p class="b">We use Infrared images to disclose possible hidden problem areas.</p>
        <p class="b">This Mold area is the result of a "Ice Dam Leak" roof leak as pictured here.</p>
        <p class="b">We adhere to <u>All industry standards</u>.</p>
      </div>
      <div class="photos">
        <figure><img src="img/Ice_Dam_and_leak_Picture.jpg" alt="Diagram: typical ice dam and leak"><figcaption>Typical ice dam and leak</figcaption></figure>
        <figure><img src="img/Picture_in_the_atic_mold.jpg" alt="Mold in an attic from an ice dam leak"><figcaption>Attic mold from the leak</figcaption></figure>
      </div>
    </div>
    <div class="closing"><p class="b red">Office: {TEL1} &nbsp; Direct/Text: {TEL2}</p></div>'''
side=f'''
    <div class="licensed">INSURED &amp; LICENSED</div>
    {LOGO}
    <a class="tell" href="about.html">Click here<br>To Learn<br>About Us!</a>
    {CALLUS}
    {vid('ERQej_DRHCE','New York Residents')}
    {BLACKMOLD}
    <div class="sealrow" style="margin-top:14px">{GREENBIZ}</div>'''
pages['partner']=('Partners',[vid('1Jl-C5-OQ5M','2017 Air Marshalls'),vid('ERQej_DRHCE','New York Residents'),vid('gciSp5X40t0','Air Marshalls Environmental')],main,side)

# ================= CONTACT =================
main=f'''
    <h1>Contact Us</h1>
    <p class="b red">"A+ Five (5) Star" Rating in Value, Customer Satisfaction, Report Accuracy, Job Efficiency and Proficiency.</p>
    <p class="b"><span class="red">Asbestos, Radon</span>, Methane, Soil Gas, Industrial Indoor Air Quality Exposure Assessment Sampling</p>
    <div class="row2">
      <div>
        {figrow('Picture_office_building1.jpg','Office building','<p class="b" style="margin-bottom:4px">Licensed, Insured, Certified, Respected and Professional</p><p>Air Marshalls Environmental Consultants are licensed insured certified professional consultants and are HIGHLY respected throughout the Indoor Air Quality industry.</p><p class="award">GREEN - LEED Credit 3.2 Indoor Air Quality Test Sampling</p>',sm=True)}
        {figrow('High_rise_bldg_Picture.jpg','High-rise building','<p class="b" style="margin-bottom:4px">Systematic Inspections yield Systematic Solutions</p><p>Air Marshalls Environmental Consultants systematically assess all situations/concerns, write protocols, and offer preventative measures.</p><p class="award">Best of "Professional Services" Award Winner!</p>',sm=True)}
        {figrow('Copy_of_House_Picture1.jpg','Residential home','<p class="b" style="margin-bottom:4px">Over 35 years of Experience</p><p>Teaching and Training Systematic (Fact Finding) Problem Solving. We take great pride in being prompt professionals and delivering exceptional service to our <u>residential</u> and <u>commercial</u> clients.</p><p class="award">Best of "Professional Services" Award Winner!</p>',sm=True)}
      </div>
      <div>
        <h3 style="margin-top:0">Please fill out the form below, we will contact you as soon as possible.</h3>
        {form(['Name','Email','Comments'])}
      </div>
    </div>
    <p style="margin-top:16px">Air Marshalls Environmental Consultants offers Assessments and Inspections using <b>IR-Fusion Technology Infrared Thermal Imaging</b> Moisture Detection.</p>
    <p class="b">Systematic (Fact Finding) Root Cause Problem Solving</p>
    <p class="b green" style="font-style:italic;text-decoration:underline">Air Marshalls Environmental uses Accredited Independent Laboratory services ONLY!</p>
    <p><b style="color:var(--blue)">Air Marshalls Environmental Licensed Certified Consultants</b> are equipped and trained in the use of the latest technologies choose your report format from one or each of the above.</p>
    <div class="row2" style="grid-template-columns:1fr 340px">
      <div>
        <ul>
          <li class="b">Voice to Text Reporting Software</li>
          <li class="b">Thermal Infrared Imaging Camera</li>
          <li class="b">Protimeter MMS Moisture Meter</li>
        </ul>
        <p class="b" style="color:var(--blue);margin-top:10px">Air Marshalls Environmental Licensed Certified Consultants are trained and equipped with the latest Moisture Detection Equipment and Technology.</p>
        <p class="b red" style="font-style:italic;text-decoration:underline">Compressed Air Quality, Radon, Methane, Sampling.</p>
      </div>
      <div class="photos">
        <figure><img src="img/contact_element57.jpg" alt="Protimeter moisture meter reading"><figcaption>Protimeter MMS moisture meter</figcaption></figure>
        <figure><img src="img/2009_07_16_voice_to_text_pic_1.jpg" alt="Voice to text reporting" style="object-fit:contain;background:#fff"><figcaption>Voice-to-text reporting</figcaption></figure>
        <figure class="wide"><img src="img/residential_pic_4.jpg" alt="Thermal image: tested wet, high moisture reading"><figcaption class="b red">Tested Wet, High Moisture Reading</figcaption></figure>
      </div>
    </div>
    <div class="closing">
      <h3 style="margin-top:0">Call Us Today:</h3>
      <p class="b" style="color:var(--blue);font-style:italic">Air Marshalls Environmental Professionals</p>
      <p><b>Office:</b> {TEL1}<br><b class="red">Direct / Text:</b> {TEL2}<br><b>Email us at:</b> {MAIL}</p>
      <p class="b">Air Marshalls Environmental Consultants<br><span style="font-weight:normal">LICENSED CERTIFIED Indoor Air Quality CONSULTING &amp; ASSESSMENTS.</span></p>
      <p class="award">Best of "Professional Services" Award Winner!</p>
    </div>'''
side=f'''
    {LIC}
    {LOGO}
    <img class="qr" src="img/2013_03_23_Chart_Air_Marshalls_Environmental.jpg" alt="QR code for airmarshallsenvironmental.org">
    {TELL}{LADY}{CALLUS}
    {BLACKMOLD}
    <div class="sealrow" style="margin-top:14px">{OSHA}</div>'''
pages['contact']=('Contact Us',[vid('By1R3_OJHyA','2017 Air Marshalls'),vid('1Jl-C5-OQ5M','Air Marshalls OSHA Industrial Hygiene'),vid('gciSp5X40t0','Air Marshalls Environmental')],main,side)

for slug,(title,videos,main,side) in pages.items():
    open(f'{OUT}/{slug}.html','w').write(shell(slug,title,videos,main,side))
    print('wrote',slug, os.path.getsize(f'{OUT}/{slug}.html'))

# ---------- extras for hosting ----------
open(f'{OUT}/CNAME','w').write('www.airmarshallsenvironmental.org\n')
open(f'{OUT}/robots.txt','w').write('User-agent: *\nAllow: /\nSitemap: https://www.airmarshallsenvironmental.org/sitemap.xml\n')
urls=''.join(f'  <url><loc>https://www.airmarshallsenvironmental.org/{"" if s_=="index" else s_+".html"}</loc></url>\n' for s_,_ in [('index','Home'),('services','Services'),('about','About Us'),('about_mold','About Mold'),('partner','Partners'),('contact','Contact Us')])
open(f'{OUT}/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+urls+'</urlset>\n')
open(f'{OUT}/404.html','w').write(shell('404','Page not found',[],'''
    <h1>That page has moved</h1>
    <p class="lead">Use the menu above, or call us and we will point you the right way.</p>
    <p class="b red">Office: 855-825-7770 &nbsp; Direct / Text: 318-288-5363</p>''','''
    <div class="licensed">LICENSED &amp; INSURED!</div>
    <img class="logo" src="img/logo_big.jpg" alt="Air Marshalls Environmental">'''))
print('extras written')
