# -*- coding: utf-8 -*-
section_symbol = '\xc2\xa7'  # § -- omg unicode wtf

remittance_advice_codes = {
    "M1": ("X-ray not taken within the past 12 months or near enough "
        "to the start of treatment."),
    "M2": ("Not paid separately when the patient is an inpatient."),
    "M3": ("Equipment is the same or similar to equipment already "
        "being used."),
    "M4": ("Alert: This is the last monthly installment payment for "
        "this durable medical equipment."),
    "M5": ("Monthly rental payments can continue until the earlier of "
        "the 15th month from the first rental month, or the month when the "
        "equipment is no longer needed."),
    "M6": ("Alert: You must furnish and service this item for any "
        "period of medical need for the remainder of the reasonable useful "
        "lifetime of the equipment."),
    "M7": ("No rental payments after the item is purchased, or after "
        "the total of issued rental payments equals the purchase price."),
    "M8": ("We do not accept blood gas tests results when the test was "
        "conducted by a medical supplier or taken while the patient is on "
        "oxygen."),
    "M9": ("Alert: This is the tenth rental month. You must offer the "
        "patient the choice of changing the rental to a purchase "
        "agreement."),
    "M10": ("Equipment purchases are limited to the first or the tenth "
        "month of medical necessity."),
    "M11": ("DME, orthotics and prosthetics must be billed to the DME "
        "carrier who services the patient's zip code."),
    "M12": ("Diagnostic tests performed by a physician must indicate "
        "whether purchased services are included on the claim."),
    "M13": ("Only one initial visit is covered per specialty per "
        "medical group."),
    "M14": ("No separate payment for an injection administered during "
        "an office visit, and no payment for a full office visit if the "
        "patient only received an injection."),
    "M15": ("Separately billed services/tests have been bundled as "
        "they are considered components of the same procedure. Separate "
        "payment is not allowed."),
    "M16": ("Alert: Please see our web site, mailings, or bulletins "
        "for more details concerning this policy/procedure/decision."),
    "M17": ("Alert: Payment approved as you did not know, and could "
        "not reasonably have been expected to know, that this would not "
        "normally have been covered for this patient. In the future, you "
        "will be liable for charges for the same service(s) under the same "
        "or similar conditions."),
    "M18": ("Certain services may be approved for home use. Neither a "
        "hospital nor a Skilled Nursing Facility (SNF) is considered to be "
        "a patient's home."),
    "M19": ("Missing oxygen certification/re-certification."),
    "M20": ("Missing/incomplete/invalid HCPCS."),
    "M21": ("Missing/incomplete/invalid place of residence for this "
        "service/item provided in a home."),
    "M22": ("Missing/incomplete/invalid number of miles traveled."),
    "M23": ("Missing invoice."),
    "M24": ("Missing/incomplete/invalid number of doses per vial."),
    "M25": ("The information furnished does not substantiate the need "
        "for this level of service. If you believe the service should have "
        "been fully covered as billed, or if you did not know and could not "
        "reasonably have been expected to know that we would not pay for "
        "this level of service, or if you notified the patient in writing "
        "in advance that we would not pay for this level of service and "
        "he/she agreed in writing to pay, ask us to review your claim "
        "within 120 days of the date of this notice. If you do not request "
        "an appeal, we will, upon application from the patient, reimburse "
        "him/her for the amount you have collected from him/her in excess "
        "of any deductible and coinsurance amounts. We will recover the "
        "reimbursement from you as an overpayment."),
    "M26": ("The information furnished does not substantiate the need "
        "for this level of service. If you have collected any amount from "
        "the patient for this level of service /any amount that exceeds the "
        "limiting charge for the less extensive service, the law requires "
        "you to refund that amount to the patient within 30 days of "
        "receiving this notice. \n\nThe requirements for refund are in "
        "1824(I) of the Social Security Act and 42CFR411.408. The section "
        "specifies that physicians who knowingly and willfully fail to make "
        "appropriate refunds may be subject to civil monetary penalties "
        "and/or exclusion from the program. If you have any questions about "
        "this notice, please contact this office."),
    "M27": ("Alert: The patient has been relieved of liability of "
        "payment of these items and services under the limitation of "
        "liability provision of the law. The provider is ultimately liable "
        "for the patient's waived charges, including any charges for "
        "coinsurance, since the items or services were not reasonable and "
        "necessary or constituted custodial care, and you knew or could "
        "reasonably have been expected to know, that they were not covered. "
        "You may appeal this determination. You may ask for an appeal "
        "regarding both the coverage determination and the issue of whether "
        "you exercised due care. The appeal request must be filed within "
        "120 days of the date you receive this notice. You must make the "
        "request through this office."),
    "M28": ("This does not qualify for payment under Part B when Part "
        "A coverage is exhausted or not otherwise available."),
    "M29": ("Missing operative note/report."),
    "M30": ("Missing pathology report."),
    "M31": ("Missing radiology report."),
    "M32": ("Alert: This is a conditional payment made pending a "
        "decision on this service by the patient's primary payer. This "
        "payment may be subject to refund upon your receipt of any "
        "additional payment for this service from another payer. You must "
        "contact this office immediately upon receipt of an additional "
        "payment for this service."),
    "M36": ("This is the 11th rental month. We cannot pay for this "
        "until you indicate that the patient has been given the option of "
        "changing the rental to a purchase."),
    "M37": ("Not covered when the patient is under age 35."),
    "M38": ("The patient is liable for the charges for this service as "
        "you informed the patient in writing before the service was "
        "furnished that we would not pay for it, and the patient agreed to "
        "pay."),
    "M39": ("The patient is not liable for payment for this service as "
        "the advance notice of non-coverage you provided the patient did "
        "not comply with program requirements."),
    "M40": ("Claim must be assigned and must be filed by the "
        "practitioner's employer."),
    "M41": ("We do not pay for this as the patient has no legal "
        "obligation to pay for this."),
    "M42": ("The medical necessity form must be personally signed by "
        "the attending physician."),
    "M44": ("Missing/incomplete/invalid condition code."),
    "M45": ("Missing/incomplete/invalid occurrence code(s)."),
    "M46": ("Missing/incomplete/invalid occurrence span code(s)."),
    "M47": ("Missing/incomplete/invalid internal or document control "
        "number."),
    "M49": ("Missing/incomplete/invalid value code(s) or amount(s)."),
    "M50": ("Missing/incomplete/invalid revenue code(s)."),
    "M51": ("Missing/incomplete/invalid procedure code(s)."),
    "M52": ("Missing/incomplete/invalid \"from\" date(s) of service."),
    "M53": ("Missing/incomplete/invalid days or units of service."),
    "M54": ("Missing/incomplete/invalid total charges."),
    "M55": ("We do not pay for self-administered anti-emetic drugs "
        "that are not administered with a covered oral anti-cancer drug."),
    "M56": ("Missing/incomplete/invalid payer identifier."),
    "M59": ("Missing/incomplete/invalid \"to\" date(s) of service."),
    "M60": ("Missing Certificate of Medical Necessity."),
    "M61": ("We cannot pay for this as the approval period for the FDA "
        "clinical trial has expired."),
    "M62": ("Missing/incomplete/invalid treatment authorization "
        "code."),
    "M64": ("Missing/incomplete/invalid other diagnosis."),
    "M65": ("One interpreting physician charge can be submitted per "
        "claim when a purchased diagnostic test is indicated. Please submit "
        "a separate claim for each interpreting physician."),
    "M66": ("Our records indicate that you billed diagnostic tests "
        "subject to price limitations and the procedure code submitted "
        "includes a professional component. Only the technical component is "
        "subject to price limitations. Please submit the technical and "
        "professional components of this service as separate line items."),
    "M67": ("Missing/incomplete/invalid other procedure code(s)."),
    "M69": ("Paid at the regular rate as you did not submit "
        "documentation to justify the modified procedure code."),
    "M70": ("Alert: The NDC code submitted for this service was "
        "translated to a HCPCS code for processing, but please continue to "
        "submit the NDC on future claims for this item."),
    "M71": ("Total payment reduced due to overlap of tests billed."),
    "M73": ("The HPSA/Physician Scarcity bonus can only be paid on the "
        "professional component of this service. Rebill as separate "
        "professional and technical components."),
    "M74": ("This service does not qualify for a HPSA/Physician "
        "Scarcity bonus payment."),
    "M75": ("Multiple automated multichannel tests performed on the "
        "same day combined for payment."),
    "M76": ("Missing/incomplete/invalid diagnosis or condition."),
    "M77": ("Missing/incomplete/invalid place of service."),
    "M79": ("Missing/incomplete/invalid charge."),
    "M80": ("Not covered when performed during the same session/date "
        "as a previously processed service for the patient."),
    "M81": ("You are required to code to the highest level of "
        "specificity."),
    "M82": ("Service is not covered when patient is under age 50."),
    "M83": ("Service is not covered unless the patient is classified "
        "as at high risk."),
    "M84": ("Medical code sets used must be the codes in effect at the "
        "time of service"),
    "M85": ("Subjected to review of physician evaluation and "
        "management services."),
    "M86": ("Service denied because payment already made for "
        "same/similar procedure within set time frame."),
    "M87": ("Claim/service(s) subjected to CFO-CAP prepayment "
        "review."),
    "M89": ("Not covered more than once under age 40."),
    "M90": ("Not covered more than once in a 12 month period."),
    "M91": ("Lab procedures with different CLIA certification numbers "
        "must be billed on separate claims."),
    "M93": ("Information supplied supports a break in therapy. A new "
        "capped rental period began with delivery of this equipment."),
    "M94": ("Information supplied does not support a break in therapy. "
        "A new capped rental period will not begin."),
    "M95": ("Services subjected to Home Health Initiative medical "
        "review/cost report audit."),
    "M96": ("The technical component of a service furnished to an "
        "inpatient may only be billed by that inpatient facility. You must "
        "contact the inpatient facility for technical component "
        "reimbursement. If not already billed, you should bill us for the "
        "professional component only."),
    "M97": ("Not paid to practitioner when provided to patient in this "
        "place of service. Payment included in the reimbursement issued the "
        "facility."),
    "M99": ("Missing/incomplete/invalid Universal Product "
        "Number/Serial Number."),
    "M100": ("We do not pay for an oral anti-emetic drug that is not "
        "administered for use immediately before, at, or within 48 hours of "
        "administration of a covered chemotherapy drug."),
    "M102": ("Service not performed on equipment approved by the FDA "
        "for this purpose."),
    "M103": ("Information supplied supports a break in therapy. "
        "However, the medical information we have for this patient does not "
        "support the need for this item as billed. We have approved payment "
        "for this item at a reduced level, and a new capped rental period "
        "will begin with the delivery of this equipment."),
    "M104": ("Information supplied supports a break in therapy. A new "
        "capped rental period will begin with delivery of the equipment. "
        "This is the maximum approved under the fee schedule for this item "
        "or service."),
    "M105": ("Information supplied does not support a break in "
        "therapy. The medical information we have for this patient does not "
        "support the need for this item as billed. We have approved payment "
        "for this item at a reduced level, and a new capped rental period "
        "will not begin."),
    "M107": ("Payment reduced as 90-day rolling average hematocrit for "
        "ESRD patient exceeded 36.5%."),
    "M109": ("We have provided you with a bundled payment for a "
        "teleconsultation. You must send 25 percent of the teleconsultation "
        "payment to the referring practitioner."),
    "M111": ("We do not pay for chiropractic manipulative treatment "
        "when the patient refuses to have an x-ray taken."),
    "M112": ("Reimbursement for this item is based on the single "
        "payment amount required under the DMEPOS Competitive Bidding "
        "Program for the area where the patient resides."),
    "M113": ("Our records indicate that this patient began using this "
        "item/service prior to the current contract period for the DMEPOS "
        "Competitive Bidding Program."),
    "M114": ("This service was processed in accordance with rules and "
        "guidelines under the DMEPOS Competitive Bidding Program or a "
        "Demonstration Project. For more information regarding these "
        "projects, contact your local contractor."),
    "M115": ("This item is denied when provided to this patient by a "
        "non-contract or non-demonstration supplier."),
    "M116": ("Processed under a demonstration project or program. "
        "Project or program is ending and additional services may not be "
        "paid under this project or program."),
    "M117": ("Not covered unless submitted via electronic claim."),
    "M119": ("Missing/incomplete/invalid/ deactivated/withdrawn "
        "National Drug Code (NDC)."),
    "M121": ("We pay for this service only when performed with a "
        "covered cryosurgical ablation."),
    "M122": ("Missing/incomplete/invalid level of subluxation."),
    "M123": ("Missing/incomplete/invalid name, strength, or dosage of "
        "the drug furnished."),
    "M124": ("Missing indication of whether the patient owns the "
        "equipment that requires the part or supply."),
    "M125": ("Missing/incomplete/invalid information on the period of "
        "time for which the service/supply/equipment will be needed."),
    "M126": ("Missing/incomplete/invalid individual lab codes included "
        "in the test."),
    "M127": ("Missing patient medical record for this service."),
    "M129": ("Missing/incomplete/invalid indicator of x-ray "
        "availability for review."),
    "M130": ("Missing invoice or statement certifying the actual cost "
        "of the lens, less discounts, and/or the type of intraocular lens "
        "used."),
    "M131": ("Missing physician financial relationship form."),
    "M132": ("Missing pacemaker registration form."),
    "M133": ("Claim did not identify who performed the purchased "
        "diagnostic test or the amount you were charged for the test."),
    "M134": ("Performed by a facility/supplier in which the provider "
        "has a financial interest."),
    "M135": ("Missing/incomplete/invalid plan of treatment."),
    "M136": ("Missing/incomplete/invalid indication that the service "
        "was supervised or evaluated by a physician."),
    "M137": ("Part B coinsurance under a demonstration project."),
    "M138": ("Patient identified as a demonstration participant but "
        "the patient was not enrolled in the demonstration at the time "
        "services were rendered. Coverage is limited to demonstration "
        "participants."),
    "M139": ("Denied services exceed the coverage limit for the "
        "demonstration."),
    "M141": ("Missing physician certified plan of care."),
    "M142": ("Missing American Diabetes Association Certificate of "
        "Recognition."),
    "M143": ("The provider must update license information with the "
        "payer."),
    "M144": ("Pre-/post-operative care payment is included in the "
        "allowance for the surgery/procedure."),
    "MA01": ("Alert: If you do not agree with what we approved for "
        "these services, you may appeal our decision. To make sure that we "
        "are fair to you, we require another individual that did not "
        "process your initial claim to conduct the appeal. However, in "
        "order to be eligible for an appeal, you must write to us within "
        "120 days of the date you received this notice, unless you have a "
        "good reason for being late."),
    "MA02": ("Alert: If you do not agree with this determination, you "
        "have the right to appeal. You must file a written request for an "
        "appeal within 180 days of the date you receive this notice."),
    "MA04": ("Secondary payment cannot be considered without the "
        "identity of or payment information from the primary payer. The "
        "information was either not reported or was illegible."),
    "MA07": ("Alert: The claim information has also been forwarded to "
        "Medicaid for review."),
    "MA08": ("Alert: Claim information was not forwarded because the "
        "supplemental coverage is not with a Medigap plan, or you do not "
        "participate in Medicare."),
    "MA09": ("Claim submitted as unassigned but processed as assigned. "
        "You agreed to accept assignment for all claims."),
    "MA10": ("Alert: The patient's payment was in excess of the amount "
        "owed. You must refund the overpayment to the patient."),
    "MA12": ("You have not established that you have the right under "
        "the law to bill for services furnished by the person(s) that "
        "furnished this (these) service(s)."),
    "MA13": ("Alert: You may be subject to penalties if you bill the "
        "patient for amounts not reported with the PR (patient "
        "responsibility) group code."),
    "MA14": ("Alert: The patient is a member of an employer-sponsored "
        "prepaid health plan. Services from outside that health plan are "
        "not covered. However, as you were not previously notified of this, "
        "we are paying this time. In the future, we will not pay you for "
        "non-plan services."),
    "MA15": ("Alert: Your claim has been separated to expedite "
        "handling. You will receive a separate notice for the other "
        "services reported."),
    "MA16": ("The patient is covered by the Black Lung Program. Send "
        "this claim to the Department of Labor, Federal Black Lung Program, "
        "P.O. Box 828, Lanham-Seabrook MD 20703."),
    "MA17": ("We are the primary payer and have paid at the primary "
        "rate. You must contact the patient's other insurer to refund any "
        "excess it may have paid due to its erroneous primary payment."),
    "MA18": ("Alert: The claim information is also being forwarded to "
        "the patient's supplemental insurer. Send any questions regarding "
        "supplemental benefits to them."),
    "MA19": ("Alert: Information was not sent to the Medigap insurer "
        "due to incorrect/invalid information you submitted concerning that "
        "insurer. Please verify your information and submit your secondary "
        "claim directly to that insurer."),
    "MA20": ("Skilled Nursing Facility (SNF) stay not covered when "
        "care is primarily related to the use of an urethral catheter for "
        "convenience or the control of incontinence."),
    "MA21": ("SSA records indicate mismatch with name and sex."),
    "MA22": ("Payment of less than $1.00 suppressed."),
    "MA23": ("Demand bill approved as result of medical review."),
    "MA24": ("Christian Science Sanitarium/ Skilled Nursing Facility "
        "(SNF) bill in the same benefit period."),
    "MA25": ("A patient may not elect to change a hospice provider "
        "more than once in a benefit period."),
    "MA26": ("Alert: Our records indicate that you were previously "
        "informed of this rule."),
    "MA27": ("Missing/incomplete/invalid entitlement number or name "
        "shown on the claim."),
    "MA28": ("Alert: Receipt of this notice by a physician or supplier "
        "who did not accept assignment is for information only and does not "
        "make the physician or supplier a party to the determination. No "
        "additional rights to appeal this decision, above those rights "
        "already provided for by regulation/instruction, are conferred by "
        "receipt of this notice."),
    "MA30": ("Missing/incomplete/invalid type of bill."),
    "MA31": ("Missing/incomplete/invalid beginning and ending dates of "
        "the period billed."),
    "MA32": ("Missing/incomplete/invalid number of covered days during "
        "the billing period."),
    "MA33": ("Missing/incomplete/invalid noncovered days during the "
        "billing period."),
    "MA34": ("Missing/incomplete/invalid number of coinsurance days "
        "during the billing period."),
    "MA35": ("Missing/incomplete/invalid number of lifetime reserve "
        "days."),
    "MA36": ("Missing/incomplete/invalid patient name."),
    "MA37": ("Missing/incomplete/invalid patient's address."),
    "MA39": ("Missing/incomplete/invalid gender."),
    "MA40": ("Missing/incomplete/invalid admission date."),
    "MA41": ("Missing/incomplete/invalid admission type."),
    "MA42": ("Missing/incomplete/invalid admission source."),
    "MA43": ("Missing/incomplete/invalid patient status."),
    "MA44": ("Alert: No appeal rights. Adjudicative decision based on "
        "law."),
    "MA45": ("Alert: As previously advised, a portion or all of your "
        "payment is being held in a special account."),
    "MA46": ("The new information was considered but additional "
        "payment will not be issued."),
    "MA47": ("Our records show you have opted out of Medicare, "
        "agreeing with the patient not to bill Medicare for "
        "services/tests/supplies furnished. As result, we cannot pay this "
        "claim. The patient is responsible for payment."),
    "MA48": ("Missing/incomplete/invalid name or address of "
        "responsible party or primary payer."),
    "MA50": ("Missing/incomplete/invalid Investigational Device "
        "Exemption number for FDA-approved clinical trial services."),
    "MA53": ("Missing/incomplete/invalid Competitive Bidding "
        "Demonstration Project identification."),
    "MA54": ("Physician certification or election consent for hospice "
        "care not received timely."),
    "MA55": ("Not covered as patient received medical health care "
        "services, automatically revoking his/her election to receive "
        "religious non-medical health care services."),
    "MA56": ("Our records show you have opted out of Medicare, "
        "agreeing with the patient not to bill Medicare for "
        "services/tests/supplies furnished. As result, we cannot pay this "
        "claim. The patient is responsible for payment, but under Federal "
        "law, you cannot charge the patient more than the limiting charge "
        "amount."),
    "MA57": ("Patient submitted written request to revoke his/her "
        "election for religious non-medical health care services."),
    "MA58": ("Missing/incomplete/invalid release of information "
        "indicator."),
    "MA59": ("Alert: The patient overpaid you for these services. You "
        "must issue the patient a refund within 30 days for the difference "
        "between his/her payment and the total amount shown as patient "
        "responsibility on this notice."),
    "MA60": ("Missing/incomplete/invalid patient relationship to "
        "insured."),
    "MA61": ("Missing/incomplete/invalid social security number or "
        "health insurance claim number."),
    "MA62": ("Alert: This is a telephone review decision."),
    "MA63": ("Missing/incomplete/invalid principal diagnosis."),
    "MA64": ("Our records indicate that we should be the third payer "
        "for this claim. We cannot process this claim until we have "
        "received payment information from the primary and secondary "
        "payers."),
    "MA65": ("Missing/incomplete/invalid admitting diagnosis."),
    "MA66": ("Missing/incomplete/invalid principal procedure code."),
    "MA67": ("Correction to a prior claim."),
    "MA68": ("Alert: We did not crossover this claim because the "
        "secondary insurance information on the claim was incomplete. "
        "Please supply complete information or use the PLANID of the "
        "insurer to assure correct and timely routing of the claim."),
    "MA69": ("Missing/incomplete/invalid remarks."),
    "MA70": ("Missing/incomplete/invalid provider representative "
        "signature."),
    "MA71": ("Missing/incomplete/invalid provider representative "
        "signature date."),
    "MA72": ("Alert: The patient overpaid you for these assigned "
        "services. You must issue the patient a refund within 30 days for "
        "the difference between his/her payment to you and the total of the "
        "amount shown as patient responsibility and as paid to the patient "
        "on this notice."),
    "MA73": ("Informational remittance associated with a Medicare "
        "demonstration. No payment issued under fee-for-service Medicare as "
        "patient has elected managed care."),
    "MA74": ("This payment replaces an earlier payment for this claim "
        "that was either lost, damaged or returned."),
    "MA75": ("Missing/incomplete/invalid patient or authorized "
        "representative signature."),
    "MA76": ("Missing/incomplete/invalid provider identifier for home "
        "health agency or hospice when physician is performing care plan "
        "oversight services."),
    "MA77": ("Alert: The patient overpaid you. You must issue the "
        "patient a refund within 30 days for the difference between the "
        "patient's payment less the total of our and other payer payments "
        "and the amount shown as patient responsibility on this notice."),
    "MA79": ("Billed in excess of interim rate."),
    "MA80": ("Informational notice. No payment issued for this claim "
        "with this notice. Payment issued to the hospital by its "
        "intermediary for all services for this encounter under a "
        "demonstration project."),
    "MA81": ("Missing/incomplete/invalid provider/supplier "
        "signature."),
    "MA83": ("Did not indicate whether we are the primary or secondary "
        "payer."),
    "MA84": ("Patient identified as participating in the National "
        "Emphysema Treatment Trial but our records indicate that this "
        "patient is either not a participant, or has not yet been approved "
        "for this phase of the study. Contact Johns Hopkins University, the "
        "study coordinator, to resolve if there was a discrepancy."),
    "MA88": ("Missing/incomplete/invalid insured's address and/or "
        "telephone number for the primary payer."),
    "MA89": ("Missing/incomplete/invalid patient's relationship to the "
        "insured for the primary payer."),
    "MA90": ("Missing/incomplete/invalid employment status code for "
        "the primary insured."),
    "MA91": ("This determination is the result of the appeal you "
        "filed."),
    "MA92": ("Missing plan information for other insurance."),
    "MA93": ("Non-PIP (Periodic Interim Payment) claim."),
    "MA94": ("Did not enter the statement \"Attending physician not "
        "hospice employee\" on the claim form to certify that the rendering "
        "physician is not an employee of the hospice."),
    "MA96": ("Claim rejected. Coded as a Medicare Managed Care "
        "Demonstration but patient is not enrolled in a Medicare managed "
        "care plan."),
    "MA97": ("Missing/incomplete/invalid Medicare Managed Care "
        "Demonstration contract number or clinical trial registry "
        "number."),
    "MA99": ("Missing/incomplete/invalid Medigap information."),
    "MA100": ("Missing/incomplete/invalid date of current illness or "
        "symptoms"),
    "MA103": ("Hemophilia Add On."),
    "MA106": ("PIP (Periodic Interim Payment) claim."),
    "MA107": ("Paper claim contains more than three separate data "
        "items in field 19."),
    "MA108": ("Paper claim contains more than one data item in field "
        "23."),
    "MA109": ("Claim processed in accordance with ambulatory surgical "
        "guidelines."),
    "MA110": ("Missing/incomplete/invalid information on whether the "
        "diagnostic test(s) were performed by an outside entity or if no "
        "purchased tests are included on the claim."),
    "MA111": ("Missing/incomplete/invalid purchase price of the "
        "test(s) and/or the performing laboratory's name and address."),
    "MA112": ("Missing/incomplete/invalid group practice "
        "information."),
    "MA113": ("Incomplete/invalid taxpayer identification number (TIN) "
        "submitted by you per the Internal Revenue Service. Your claims "
        "cannot be processed without your correct TIN, and you may not bill "
        "the patient pending correction of your TIN. There are no appeal "
        "rights for unprocessable claims, but you may resubmit this claim "
        "after you have notified this office of your correct TIN."),
    "MA114": ("Missing/incomplete/invalid information on where the "
        "services were furnished."),
    "MA115": ("Missing/incomplete/invalid physical location (name and "
        "address, or PIN) where the service(s) were rendered in a Health "
        "Professional Shortage Area (HPSA)."),
    "MA116": ("Did not complete the statement 'Homebound' on the claim "
        "to validate whether laboratory services were performed at home or "
        "in an institution."),
    "MA117": ("This claim has been assessed a $1.00 user fee."),
    "MA118": ("Coinsurance and/or deductible amounts apply to a claim "
        "for services or supplies furnished to a Medicare-eligible veteran "
        "through a facility of the Department of Veterans Affairs. No "
        "Medicare payment issued."),
    "MA120": ("Missing/incomplete/invalid CLIA certification "
        "number."),
    "MA121": ("Missing/incomplete/invalid x-ray date."),
    "MA122": ("Missing/incomplete/invalid initial treatment date."),
    "MA123": ("Your center was not selected to participate in this "
        "study, therefore, we cannot pay for these services."),
    "MA125": ("Per legislation governing this program, payment "
        "constitutes payment in full."),
    "MA126": ("Pancreas transplant not covered unless kidney "
        "transplant performed."),
    "MA128": ("Missing/incomplete/invalid FDA approval number."),
    "MA130": ("Your claim contains incomplete and/or invalid "
        "information, and no appeal rights are afforded because the claim "
        "is unprocessable. Please submit a new claim with the "
        "complete/correct information."),
    "MA131": ("Physician already paid for services in conjunction with "
        "this demonstration claim. You must have the physician withdraw "
        "that claim and refund the payment before we can process your "
        "claim."),
    "MA132": ("Adjustment to the pre-demonstration rate."),
    "MA133": ("Claim overlaps inpatient stay. Rebill only those "
        "services rendered outside the inpatient stay."),
    "MA134": ("Missing/incomplete/invalid provider number of the "
        "facility where the patient resides."),
    "N1": ("Alert: You may appeal this decision in writing within the "
        "required time limits following receipt of this notice by following "
        "the instructions included in your contract or plan benefit "
        "documents."),
    "N2": ("This allowance has been made in accordance with the most "
        "appropriate course of treatment provision of the plan."),
    "N3": ("Missing consent form."),
    "N4": ("Missing/Incomplete/Invalid prior Insurance Carrier(s) "
        "EOB."),
    "N5": ("EOB received from previous payer. Claim not on file."),
    "N6": ("Under FEHB law (U.S.C. 8904(b)), we cannot pay more for "
        "covered care than the amount Medicare would have allowed if the "
        "patient were enrolled in Medicare Part A and/or Medicare Part "
        "B."),
    "N7": ("Processing of this claim/service has included "
        "consideration under Major Medical provisions."),
    "N8": ("Crossover claim denied by previous payer and complete "
        "claim data not forwarded. Resubmit this claim to this payer to "
        "provide adequate data for adjudication."),
    "N9": ("Adjustment represents the estimated amount a previous "
        "payer may pay."),
    "N10": ("Payment based on the findings of a review "
        "organization/professional consult/manual adjudication/medical or "
        "dental advisor."),
    "N11": ("Denial reversed because of medical review."),
    "N12": ("Policy provides coverage supplemental to Medicare. As the "
        "member does not appear to be enrolled in the applicable part of "
        "Medicare, the member is responsible for payment of the portion of "
        "the charge that would have been covered by Medicare."),
    "N13": ("Payment based on professional/technical component "
        "modifier(s)."),
    "N15": ("Services for a newborn must be billed separately."),
    "N16": ("Family/member Out-of-Pocket maximum has been met. Payment "
        "based on a higher percentage."),
    "N19": ("Procedure code incidental to primary procedure."),
    "N20": ("Service not payable with other service rendered on the "
        "same date."),
    "N21": ("Alert: Your line item has been separated into multiple "
        "lines to expedite handling."),
    "N22": ("This procedure code was added/changed because it more "
        "accurately describes the services rendered."),
    "N23": ("Alert: Patient liability may be affected due to "
        "coordination of benefits with other carriers and/or maximum "
        "benefit provisions."),
    "N24": ("Missing/incomplete/invalid Electronic Funds Transfer "
        "(EFT) banking information."),
    "N25": ("This company has been contracted by your benefit plan to "
        "provide administrative claims payment services only. This company "
        "does not assume financial risk or obligation with respect to "
        "claims processed on behalf of your benefit plan."),
    "N26": ("Missing itemized bill/statement."),
    "N27": ("Missing/incomplete/invalid treatment number."),
    "N28": ("Consent form requirements not fulfilled."),
    "N29": ("Missing "
        "documentation/orders/notes/summary/report/chart."),
    "N30": ("Patient ineligible for this service."),
    "N31": ("Missing/incomplete/invalid prescribing provider "
        "identifier."),
    "N32": ("Claim must be submitted by the provider who rendered the "
        "service."),
    "N33": ("No record of health check prior to initiation of "
        "treatment."),
    "N34": ("Incorrect claim form/format for this service."),
    "N35": ("Program integrity/utilization review decision."),
    "N36": ("Claim must meet primary payer's processing requirements "
        "before we can consider payment."),
    "N37": ("Missing/incomplete/invalid tooth number/letter."),
    "N39": ("Procedure code is not compatible with tooth "
        "number/letter."),
    "N40": ("Missing radiology film(s)/image(s)."),
    "N42": ("No record of mental health assessment."),
    "N43": ("Bed hold or leave days exceeded."),
    "N45": ("Payment based on authorized amount."),
    "N46": ("Missing/incomplete/invalid admission hour."),
    "N47": ("Claim conflicts with another inpatient stay."),
    "N48": ("Claim information does not agree with information "
        "received from other insurance carrier."),
    "N49": ("Court ordered coverage information needs validation."),
    "N50": ("Missing/incomplete/invalid discharge information."),
    "N51": ("Electronic interchange agreement not on file for "
        "provider/submitter."),
    "N52": ("Patient not enrolled in the billing provider's managed "
        "care plan on the date of service."),
    "N53": ("Missing/incomplete/invalid point of pick-up address."),
    "N54": ("Claim information is inconsistent with "
        "pre-certified/authorized services."),
    "N55": ("Procedures for billing with group/referring/performing "
        "providers were not followed."),
    "N56": ("Procedure code billed is not correct/valid for the "
        "services billed or the date of service billed."),
    "N57": ("Missing/incomplete/invalid prescribing date."),
    "N58": ("Missing/incomplete/invalid patient liability amount."),
    "N59": ("Please refer to your provider manual for additional "
        "program and provider information."),
    "N61": ("Rebill services on separate claims."),
    "N62": ("Dates of service span multiple rate periods. Resubmit "
        "separate claims."),
    "N63": ("Rebill services on separate claim lines."),
    "N64": ("The \"from\" and \"to\" dates must be different."),
    "N65": ("Procedure code or procedure rate count cannot be "
        "determined, or was not on file, for the date of "
        "service/provider."),
    "N67": ("Professional provider services not paid separately. "
        "Included in facility payment under a demonstration project. Apply "
        "to that facility for payment, or resubmit your claim if: the "
        "facility notifies you the patient was excluded from this "
        "demonstration; or if you furnished these services in another "
        "location on the date of the patient's admission or discharge from "
        "a demonstration hospital. If services were furnished in a facility "
        "not involved in the demonstration on the same date the patient was "
        "discharged from or admitted to a demonstration facility, you must "
        "report the provider ID number for the non-demonstration facility "
        "on the new claim."),
    "N68": ("Prior payment being cancelled as we were subsequently "
        "notified this patient was covered by a demonstration project in "
        "this site of service. Professional services were included in the "
        "payment made to the facility. You must contact the facility for "
        "your payment. Prior payment made to you by the patient or another "
        "insurer for this claim must be refunded to the payer within 30 "
        "days."),
    "N69": ("PPS (Prospective Payment System) code changed by claims "
        "processing system. Insufficient visits or therapies."),
    "N70": ("Consolidated billing and payment applies."),
    "N71": ("Your unassigned claim for a drug or biological, clinical "
        "diagnostic laboratory services or ambulance service was processed "
        "as an assigned claim. You are required by law to accept assignment "
        "for these types of claims."),
    "N72": ("PPS (Prospective Payment System) code changed by medical "
        "reviewers. Not supported by clinical records."),
    "N74": ("Resubmit with multiple claims, each claim covering "
        "services provided in only one calendar month."),
    "N75": ("Missing/incomplete/invalid tooth surface information."),
    "N76": ("Missing/incomplete/invalid number of riders."),
    "N77": ("Missing/incomplete/invalid designated provider number."),
    "N78": ("The necessary components of the child and teen checkup "
        "(EPSDT) were not completed."),
    "N79": ("Service billed is not compatible with patient location "
        "information."),
    "N80": ("Missing/incomplete/invalid prenatal screening "
        "information."),
    "N81": ("Procedure billed is not compatible with tooth surface "
        "code."),
    "N82": ("Provider must accept insurance payment as payment in full "
        "when a third party payer contract specifies full reimbursement."),
    "N83": ("No appeal rights. Adjudicative decision based on the "
        "provisions of a demonstration project."),
    "N84": ("Alert: Further installment payments are forthcoming."),
    "N85": ("Alert: This is the final installment payment."),
    "N86": ("A failed trial of pelvic muscle exercise training is "
        "required in order for biofeedback training for the treatment of "
        "urinary incontinence to be covered."),
    "N87": ("Home use of biofeedback therapy is not covered."),
    "N88": ("Alert: This payment is being made conditionally. An HHA "
        "episode of care notice has been filed for this patient. When a "
        "patient is treated under a HHA episode of care, consolidated "
        "billing requires that certain therapy services and supplies, such "
        "as this, be included in the HHA's payment. This payment will need "
        "to be recouped from you if we establish that the patient is "
        "concurrently receiving treatment under a HHA episode of care."),
    "N89": ("Alert: Payment information for this claim has been "
        "forwarded to more than one other payer, but format limitations "
        "permit only one of the secondary payers to be identified in this "
        "remittance advice."),
    "N90": ("Covered only when performed by the attending "
        "physician."),
    "N91": ("Services not included in the appeal review."),
    "N92": ("This facility is not certified for digital "
        "mammography."),
    "N93": ("A separate claim must be submitted for each place of "
        "service. Services furnished at multiple sites may not be billed in "
        "the same claim."),
    "N94": ("Claim/Service denied because a more specific taxonomy "
        "code is required for adjudication."),
    "N95": ("This provider type/provider specialty may not bill this "
        "service."),
    "N96": ("Patient must be refractory to conventional therapy "
        "(documented behavioral, pharmacologic and/or surgical corrective "
        "therapy) and be an appropriate surgical candidate such that "
        "implantation with anesthesia can occur."),
    "N97": ("Patients with stress incontinence, urinary obstruction, "
        "and specific neurologic diseases (e.g., diabetes with peripheral "
        "nerve involvement) which are associated with secondary "
        "manifestations of the above three indications are excluded."),
    "N98": ("Patient must have had a successful test stimulation in "
        "order to support subsequent implantation. Before a patient is "
        "eligible for permanent implantation, he/she must demonstrate a 50 "
        "percent or greater improvement through test stimulation. "
        "Improvement is measured through voiding diaries."),
    "N99": ("Patient must be able to demonstrate adequate ability to "
        "record voiding diary data such that clinical results of the "
        "implant procedure can be properly evaluated."),
    "N100": ("PPS (Prospect Payment System) code corrected during "
        "adjudication."),
    "N102": ("This claim has been denied without reviewing the medical "
        "record because the requested records were not received or were not "
        "received timely."),
    "N103": ("Social Security records indicate that this patient was a "
        "prisoner when the service was rendered. This payer does not cover "
        "items and services furnished to an individual while they are in "
        "State or local custody under a penal authority, unless under State "
        "or local law, the individual is personally liable for the cost of "
        "his or her health care while incarcerated and the State or local "
        "government pursues such debt in the same way and with the same "
        "vigor as any other debt."),
    "N104": ("This claim/service is not payable under our claims "
        "jurisdiction area. You can identify the correct Medicare "
        "contractor to process this claim/service through the CMS website "
        "at www.cms.gov."),
    "N105": ("This is a misdirected claim/service for an RRB "
        "beneficiary. Submit paper claims to the RRB carrier: Palmetto GBA, "
        "P.O. Box 10066, Augusta, GA 30999. Call 866-749-4301 for RRB EDI "
        "information for electronic claims processing."),
    "N106": ("Payment for services furnished to Skilled Nursing "
        "Facility (SNF) inpatients (except for excluded services) can only "
        "be made to the SNF. You must request payment from the SNF rather "
        "than the patient for this service."),
    "N107": ("Services furnished to Skilled Nursing Facility (SNF) "
        "inpatients must be billed on the inpatient claim. They cannot be "
        "billed separately as outpatient services."),
    "N108": ("Missing/incomplete/invalid upgrade information."),
    "N109": ("This claim/service was chosen for complex review and was "
        "denied after reviewing the medical records."),
    "N110": ("This facility is not certified for film mammography."),
    "N111": ("No appeal right except duplicate claim/service issue. "
        "This service was included in a claim that has been previously "
        "billed and adjudicated."),
    "N112": ("This claim is excluded from your electronic remittance "
        "advice."),
    "N113": ("Only one initial visit is covered per physician, group "
        "practice or provider."),
    "N114": ("During the transition to the Ambulance Fee Schedule, "
        "payment is based on the lesser of a blended amount calculated "
        "using a percentage of the reasonable charge/cost and fee schedule "
        "amounts, or the submitted charge for the service. You will be "
        "notified yearly what the percentages for the blended payment "
        "calculation will be."),
    "N115": ("This decision was based on a Local Coverage "
        "Determination (LCD). An LCD provides a guide to assist in "
        "determining whether a particular item or service is covered. A "
        "copy of this policy is available at www.cms.gov/mcd, or if you do "
        "not have web access, you may contact the contractor to request a "
        "copy of the LCD."),
    "N116": ("This payment is being made conditionally because the "
        "service was provided in the home, and it is possible that the "
        "patient is under a home health episode of care. When a patient is "
        "treated under a home health episode of care, consolidated billing "
        "requires that certain therapy services and supplies, such as this, "
        "be included in the home health agency's (HHA's) payment. This "
        "payment will need to be recouped from you if we establish that the "
        "patient is concurrently receiving treatment under an HHA episode "
        "of care."),
    "N117": ("This service is paid only once in a patient's "
        "lifetime."),
    "N118": ("This service is not paid if billed more than once every "
        "28 days."),
    "N119": ("This service is not paid if billed once every 28 days, "
        "and the patient has spent 5 or more consecutive days in any "
        "inpatient or Skilled /nursing Facility (SNF) within those 28 "
        "days."),
    "N120": ("Payment is subject to home health prospective payment "
        "system partial episode payment adjustment. Patient was "
        "transferred/discharged/readmitted during payment episode."),
    "N121": ("Medicare Part B does not pay for items or services "
        "provided by this type of practitioner for beneficiaries in a "
        "Medicare Part A covered Skilled Nursing Facility (SNF) stay."),
    "N122": ("Add-on code cannot be billed by itself."),
    "N123": ("This is a split service and represents a portion of the "
        "units from the originally submitted service."),
    "N124": ("Payment has been denied for the/made only for a less "
        "extensive service/item because the information furnished does not "
        "substantiate the need for the (more extensive) service/item. The "
        "patient is liable for the charges for this service/item as you "
        "informed the patient in writing before the service/item was "
        "furnished that we would not pay for it, and the patient agreed to "
        "pay."),
    "N125": ("Payment has been (denied for the/made only for a less "
        "extensive) service/item because the information furnished does not "
        "substantiate the need for the (more extensive) service/item. If "
        "you have collected any amount from the patient, you must refund "
        "that amount to the patient within 30 days of receiving this "
        "notice.\n\nThe requirements for a refund are in {0}1834(a)(18) of "
        "the Social Security Act (and in {0}{0}1834(j)(4) and 1879(h) by "
        "cross-reference to {0}1834(a)(18)). Section 1834(a)(18)(B) specifies "
        "that suppliers which knowingly and willfully fail to make "
        "appropriate refunds may be subject to civil money penalties and/or "
        "exclusion from the Medicare program. If you have any questions "
        "about this notice, please contact this office.").format(
                section_symbol),
    "N126": ("Social Security Records indicate that this individual "
        "has been deported. This payer does not cover items and services "
        "furnished to individuals who have been deported."),
    "N127": ("This is a misdirected claim/service for a United Mine "
        "Workers of America (UMWA) beneficiary. Please submit claims to "
        "them."),
    "N128": ("This amount represents the prior to coverage portion of "
        "the allowance."),
    "N129": ("Not eligible due to the patient's age."),
    "N130": ("Consult plan benefit documents/guidelines for "
        "information about restrictions for this service."),
    "N131": ("Total payments under multiple contracts cannot exceed "
        "the allowance for this service."),
    "N132": ("Alert: Payments will cease for services rendered by this "
        "US Government debarred or excluded provider after the 30 day grace "
        "period as previously notified."),
    "N133": ("Alert: Services for predetermination and services "
        "requesting payment are being processed separately."),
    "N134": ("Alert: This represents your scheduled payment for this "
        "service. If treatment has been discontinued, please contact "
        "Customer Service."),
    "N135": ("Record fees are the patient's responsibility and limited "
        "to the specified co-payment."),
    "N136": ("Alert: To obtain information on the process to file an "
        "appeal in Arizona, call the Department's Consumer Assistance "
        "Office at (602) 912-8444 or (800) 325-2548."),
    "N137": ("Alert: The provider acting on the Member's behalf, may "
        "file an appeal with the Payer. The provider, acting on the "
        "Member's behalf, may file a complaint with the State Insurance "
        "Regulatory Authority without first filing an appeal, if the "
        "coverage decision involves an urgent condition for which care has "
        "not been rendered. The address may be obtained from the State "
        "Insurance Regulatory Authority."),
    "N138": ("Alert: In the event you disagree with the Dental "
        "Advisor's opinion and have additional information relative to the "
        "case, you may submit radiographs to the Dental Advisor Unit at the "
        "subscriber's dental insurance carrier for a second Independent "
        "Dental Advisor Review."),
    "N139": ("Alert: Under the Code of Federal Regulations, Chapter "
        "32, Section 199.13 a non-participating provider is not an "
        "appropriate appealing party. Therefore, if you disagree with the "
        "Dental Advisor's opinion, you may appeal the determination if "
        "appointed in writing, by the beneficiary, to act as his/her "
        "representative. Should you be appointed as a representative, "
        "submit a copy of this letter, a signed statement explaining the "
        "matter in which you disagree, and any radiographs and relevant "
        "information to the subscriber's Dental insurance carrier within 90 "
        "days from the date of this letter."),
    "N140": ("Alert: You have not been designated as an authorized "
        "OCONUS provider therefore are not considered an appropriate "
        "appealing party. If the beneficiary has appointed you, in writing, "
        "to act as his/her representative and you disagree with the Dental "
        "Advisor's opinion, you may appeal by submitting a copy of this "
        "letter, a signed statement explaining the matter in which you "
        "disagree, and any relevant information to the subscriber's Dental "
        "insurance carrier within 90 days from the date of this letter."),
    "N141": ("The patient was not residing in a long-term care "
        "facility during all or part of the service dates billed."),
    "N142": ("The original claim was denied. Resubmit a new claim, not "
        "a replacement claim."),
    "N143": ("The patient was not in a hospice program during all or "
        "part of the service dates billed."),
    "N144": ("The rate changed during the dates of service billed."),
    "N146": ("Missing screening document."),
    "N147": ("Long term care case mix or per diem rate cannot be "
        "determined because the patient ID number is missing, incomplete, "
        "or invalid on the assignment request."),
    "N148": ("Missing/incomplete/invalid date of last menstrual "
        "period."),
    "N149": ("Rebill all applicable services on a single claim."),
    "N150": ("Missing/incomplete/invalid model number."),
    "N151": ("Telephone contact services will not be paid until the "
        "face-to-face contact requirement has been met."),
    "N152": ("Missing/incomplete/invalid replacement claim "
        "information."),
    "N153": ("Missing/incomplete/invalid room and board rate."),
    "N154": ("Alert: This payment was delayed for correction of "
        "provider's mailing address."),
    "N155": ("Alert: Our records do not indicate that other insurance "
        "is on file. Please submit other insurance information for our "
        "records."),
    "N156": ("Alert: The patient is responsible for the difference "
        "between the approved treatment and the elective treatment."),
    "N157": ("Transportation to/from this destination is not "
        "covered."),
    "N158": ("Transportation in a vehicle other than an ambulance is "
        "not covered."),
    "N159": ("Payment denied/reduced because mileage is not covered "
        "when the patient is not in the ambulance."),
    "N160": ("The patient must choose an option before a payment can "
        "be made for this procedure/ equipment/ supply/ service."),
    "N161": ("This drug/service/supply is covered only when the "
        "associated service is covered."),
    "N162": ("Alert: Although your claim was paid, you have billed for "
        "a test/specialty not included in your Laboratory Certification. "
        "Your failure to correct the laboratory certification information "
        "will result in a denial of payment in the near future."),
    "N163": ("Medical record does not support code billed per the code "
        "definition."),
    "N167": ("Charges exceed the post-transplant coverage limit."),
    "N170": ("A new/revised/renewed certificate of medical necessity "
        "is needed."),
    "N171": ("Payment for repair or replacement is not covered or has "
        "exceeded the purchase price."),
    "N172": ("The patient is not liable for the denied/adjusted "
        "charge(s) for receiving any updated service/item."),
    "N173": ("No qualifying hospital stay dates were provided for this "
        "episode of care."),
    "N174": ("This is not a covered service/procedure/ equipment/bed, "
        "however patient liability is limited to amounts shown in the "
        "adjustments under group 'PR'."),
    "N175": ("Missing review organization approval."),
    "N176": ("Services provided aboard a ship are covered only when "
        "the ship is of United States registry and is in United States "
        "waters. In addition, a doctor licensed to practice in the United "
        "States must provide the service."),
    "N177": ("Alert: We did not send this claim to patient's other "
        "insurer. They have indicated no additional payment can be made."),
    "N178": ("Missing pre-operative photos or visual field results."),
    "N179": ("Additional information has been requested from the "
        "member. The charges will be reconsidered upon receipt of that "
        "information."),
    "N180": ("This item or service does not meet the criteria for the "
        "category under which it was billed."),
    "N181": ("Additional information is required from another provider "
        "involved in this service."),
    "N182": ("This claim/service must be billed according to the "
        "schedule for this plan."),
    "N183": ("Alert: This is a predetermination advisory message, when "
        "this service is submitted for payment additional documentation as "
        "specified in plan documents will be required to process "
        "benefits."),
    "N184": ("Rebill technical and professional components "
        "separately."),
    "N185": ("Alert: Do not resubmit this claim/service."),
    "N186": ("Non-Availability Statement (NAS) required for this "
        "service. Contact the nearest Military Treatment Facility (MTF) for "
        "assistance."),
    "N187": ("Alert: You may request a review in writing within the "
        "required time limits following receipt of this notice by following "
        "the instructions included in your contract or plan benefit "
        "documents."),
    "N188": ("The approved level of care does not match the procedure "
        "code submitted."),
    "N189": ("Alert: This service has been paid as a one-time "
        "exception to the plan's benefit restrictions."),
    "N190": ("Missing contract indicator."),
    "N191": ("The provider must update insurance information directly "
        "with payer."),
    "N192": ("Patient is a Medicaid/Qualified Medicare Beneficiary."),
    "N193": ("Specific federal/state/local program may cover this "
        "service through another payer."),
    "N194": ("Technical component not paid if provider does not own "
        "the equipment used."),
    "N195": ("The technical component must be billed separately."),
    "N196": ("Alert: Patient eligible to apply for other coverage "
        "which may be primary."),
    "N197": ("The subscriber must update insurance information "
        "directly with payer."),
    "N198": ("Rendering provider must be affiliated with the pay-to "
        "provider."),
    "N199": ("Additional payment/recoupment approved based on "
        "payer-initiated review/audit."),
    "N200": ("The professional component must be billed separately."),
    "N202": ("Additional information/explanation will be sent "
        "separately"),
    "N203": ("Missing/incomplete/invalid anesthesia time/units"),
    "N204": ("Services under review for possible pre-existing "
        "condition. Send medical records for prior 12 months"),
    "N205": ("Information provided was illegible"),
    "N206": ("The supporting documentation does not match the "
        "information sent on the claim."),
    "N207": ("Missing/incomplete/invalid weight."),
    "N208": ("Missing/incomplete/invalid DRG code"),
    "N209": ("Missing/incomplete/invalid taxpayer identification "
        "number (TIN)."),
    "N210": ("Alert: You may appeal this decision"),
    "N211": ("Alert: You may not appeal this decision"),
    "N212": ("Charges processed under a Point of Service benefit"),
    "N213": ("Missing/incomplete/invalid facility/discrete unit "
        "DRG/DRG exempt status information"),
    "N214": ("Missing/incomplete/invalid history of the related "
        "initial surgical procedure(s)"),
    "N215": ("Alert: A payer providing supplemental or secondary "
        "coverage shall not require a claims determination for this service "
        "from a primary payer as a condition of making its own claims "
        "determination."),
    "N216": ("We do not offer coverage for this type of service or the "
        "patient is not enrolled in this portion of our benefit package"),
    "N217": ("We pay only one site of service per provider per "
        "claim"),
    "N218": ("You must furnish and service this item for as long as "
        "the patient continues to need it. We can pay for maintenance "
        "and/or servicing for the time period specified in the contract or "
        "coverage manual."),
    "N219": ("Payment based on previous payer's allowed amount."),
    "N220": ("Alert: See the payer's web site or contact the payer's "
        "Customer Service department to obtain forms and instructions for "
        "filing a provider dispute."),
    "N221": ("Missing Admitting History and Physical report."),
    "N222": ("Incomplete/invalid Admitting History and Physical "
        "report."),
    "N223": ("Missing documentation of benefit to the patient during "
        "initial treatment period."),
    "N224": ("Incomplete/invalid documentation of benefit to the "
        "patient during initial treatment period."),
    "N225": ("Incomplete/invalid "
        "documentation/orders/notes/summary/report/chart."),
    "N226": ("Incomplete/invalid American Diabetes Association "
        "Certificate of Recognition."),
    "N227": ("Incomplete/invalid Certificate of Medical Necessity."),
    "N228": ("Incomplete/invalid consent form."),
    "N229": ("Incomplete/invalid contract indicator."),
    "N230": ("Incomplete/invalid indication of whether the patient "
        "owns the equipment that requires the part or supply."),
    "N231": ("Incomplete/invalid invoice or statement certifying the "
        "actual cost of the lens, less discounts, and/or the type of "
        "intraocular lens used."),
    "N232": ("Incomplete/invalid itemized bill/statement."),
    "N233": ("Incomplete/invalid operative note/report."),
    "N234": ("Incomplete/invalid oxygen "
        "certification/re-certification."),
    "N235": ("Incomplete/invalid pacemaker registration form."),
    "N236": ("Incomplete/invalid pathology report."),
    "N237": ("Incomplete/invalid patient medical record for this "
        "service."),
    "N238": ("Incomplete/invalid physician certified plan of care"),
    "N239": ("Incomplete/invalid physician financial relationship "
        "form."),
    "N240": ("Incomplete/invalid radiology report."),
    "N241": ("Incomplete/invalid review organization approval."),
    "N242": ("Incomplete/invalid radiology film(s)/image(s)."),
    "N243": ("Incomplete/invalid/not approved screening document."),
    "N244": ("Incomplete/invalid pre-operative photos/visual field "
        "results."),
    "N245": ("Incomplete/invalid plan information for other "
        "insurance"),
    "N246": ("State regulated patient payment limitations apply to "
        "this service."),
    "N247": ("Missing/incomplete/invalid assistant surgeon "
        "taxonomy."),
    "N248": ("Missing/incomplete/invalid assistant surgeon name."),
    "N249": ("Missing/incomplete/invalid assistant surgeon primary "
        "identifier."),
    "N250": ("Missing/incomplete/invalid assistant surgeon secondary "
        "identifier."),
    "N251": ("Missing/incomplete/invalid attending provider "
        "taxonomy."),
    "N252": ("Missing/incomplete/invalid attending provider name."),
    "N253": ("Missing/incomplete/invalid attending provider primary "
        "identifier."),
    "N254": ("Missing/incomplete/invalid attending provider secondary "
        "identifier."),
    "N255": ("Missing/incomplete/invalid billing provider taxonomy."),
    "N256": ("Missing/incomplete/invalid billing provider/supplier "
        "name."),
    "N257": ("Missing/incomplete/invalid billing provider/supplier "
        "primary identifier."),
    "N258": ("Missing/incomplete/invalid billing provider/supplier "
        "address."),
    "N259": ("Missing/incomplete/invalid billing provider/supplier "
        "secondary identifier."),
    "N260": ("Missing/incomplete/invalid billing provider/supplier "
        "contact information."),
    "N261": ("Missing/incomplete/invalid operating provider name."),
    "N262": ("Missing/incomplete/invalid operating provider primary "
        "identifier."),
    "N263": ("Missing/incomplete/invalid operating provider secondary "
        "identifier."),
    "N264": ("Missing/incomplete/invalid ordering provider name."),
    "N265": ("Missing/incomplete/invalid ordering provider primary "
        "identifier."),
    "N266": ("Missing/incomplete/invalid ordering provider address."),
    "N267": ("Missing/incomplete/invalid ordering provider secondary "
        "identifier."),
    "N268": ("Missing/incomplete/invalid ordering provider contact "
        "information."),
    "N269": ("Missing/incomplete/invalid other provider name."),
    "N270": ("Missing/incomplete/invalid other provider primary "
        "identifier."),
    "N271": ("Missing/incomplete/invalid other provider secondary "
        "identifier."),
    "N272": ("Missing/incomplete/invalid other payer attending "
        "provider identifier."),
    "N273": ("Missing/incomplete/invalid other payer operating "
        "provider identifier."),
    "N274": ("Missing/incomplete/invalid other payer other provider "
        "identifier."),
    "N275": ("Missing/incomplete/invalid other payer purchased service "
        "provider identifier."),
    "N276": ("Missing/incomplete/invalid other payer referring "
        "provider identifier."),
    "N277": ("Missing/incomplete/invalid other payer rendering "
        "provider identifier."),
    "N278": ("Missing/incomplete/invalid other payer service facility "
        "provider identifier."),
    "N279": ("Missing/incomplete/invalid pay-to provider name."),
    "N280": ("Missing/incomplete/invalid pay-to provider primary "
        "identifier."),
    "N281": ("Missing/incomplete/invalid pay-to provider address."),
    "N282": ("Missing/incomplete/invalid pay-to provider secondary "
        "identifier."),
    "N283": ("Missing/incomplete/invalid purchased service provider "
        "identifier."),
    "N284": ("Missing/incomplete/invalid referring provider "
        "taxonomy."),
    "N285": ("Missing/incomplete/invalid referring provider name."),
    "N286": ("Missing/incomplete/invalid referring provider primary "
        "identifier."),
    "N287": ("Missing/incomplete/invalid referring provider secondary "
        "identifier."),
    "N288": ("Missing/incomplete/invalid rendering provider "
        "taxonomy."),
    "N289": ("Missing/incomplete/invalid rendering provider name."),
    "N290": ("Missing/incomplete/invalid rendering provider primary "
        "identifier."),
    "N291": ("Missing/incomplete/invalid rendering provider secondary "
        "identifier."),
    "N292": ("Missing/incomplete/invalid service facility name."),
    "N293": ("Missing/incomplete/invalid service facility primary "
        "identifier."),
    "N294": ("Missing/incomplete/invalid service facility primary "
        "address."),
    "N295": ("Missing/incomplete/invalid service facility secondary "
        "identifier."),
    "N296": ("Missing/incomplete/invalid supervising provider name."),
    "N297": ("Missing/incomplete/invalid supervising provider primary "
        "identifier."),
    "N298": ("Missing/incomplete/invalid supervising provider "
        "secondary identifier."),
    "N299": ("Missing/incomplete/invalid occurrence date(s)."),
    "N300": ("Missing/incomplete/invalid occurrence span date(s)."),
    "N301": ("Missing/incomplete/invalid procedure date(s)."),
    "N302": ("Missing/incomplete/invalid other procedure date(s)."),
    "N303": ("Missing/incomplete/invalid principal procedure date."),
    "N304": ("Missing/incomplete/invalid dispensed date."),
    "N305": ("Missing/incomplete/invalid accident date."),
    "N306": ("Missing/incomplete/invalid acute manifestation date."),
    "N307": ("Missing/incomplete/invalid adjudication or payment "
        "date."),
    "N308": ("Missing/incomplete/invalid appliance placement date."),
    "N309": ("Missing/incomplete/invalid assessment date."),
    "N310": ("Missing/incomplete/invalid assumed or relinquished care "
        "date."),
    "N311": ("Missing/incomplete/invalid authorized to return to work "
        "date."),
    "N312": ("Missing/incomplete/invalid begin therapy date."),
    "N313": ("Missing/incomplete/invalid certification revision "
        "date."),
    "N314": ("Missing/incomplete/invalid diagnosis date."),
    "N315": ("Missing/incomplete/invalid disability from date."),
    "N316": ("Missing/incomplete/invalid disability to date."),
    "N317": ("Missing/incomplete/invalid discharge hour."),
    "N318": ("Missing/incomplete/invalid discharge or end of care "
        "date."),
    "N319": ("Missing/incomplete/invalid hearing or vision "
        "prescription date."),
    "N320": ("Missing/incomplete/invalid Home Health Certification "
        "Period."),
    "N321": ("Missing/incomplete/invalid last admission period."),
    "N322": ("Missing/incomplete/invalid last certification date."),
    "N323": ("Missing/incomplete/invalid last contact date."),
    "N324": ("Missing/incomplete/invalid last seen/visit date."),
    "N325": ("Missing/incomplete/invalid last worked date."),
    "N326": ("Missing/incomplete/invalid last x-ray date."),
    "N327": ("Missing/incomplete/invalid other insured birth date."),
    "N328": ("Missing/incomplete/invalid Oxygen Saturation Test "
        "date."),
    "N329": ("Missing/incomplete/invalid patient birth date."),
    "N330": ("Missing/incomplete/invalid patient death date."),
    "N331": ("Missing/incomplete/invalid physician order date."),
    "N332": ("Missing/incomplete/invalid prior hospital discharge "
        "date."),
    "N333": ("Missing/incomplete/invalid prior placement date."),
    "N334": ("Missing/incomplete/invalid re-evaluation date"),
    "N335": ("Missing/incomplete/invalid referral date."),
    "N336": ("Missing/incomplete/invalid replacement date."),
    "N337": ("Missing/incomplete/invalid secondary diagnosis date."),
    "N338": ("Missing/incomplete/invalid shipped date."),
    "N339": ("Missing/incomplete/invalid similar illness or symptom "
        "date."),
    "N340": ("Missing/incomplete/invalid subscriber birth date."),
    "N341": ("Missing/incomplete/invalid surgery date."),
    "N342": ("Missing/incomplete/invalid test performed date."),
    "N343": ("Missing/incomplete/invalid Transcutaneous Electrical "
        "Nerve Stimulator (TENS) trial start date."),
    "N344": ("Missing/incomplete/invalid Transcutaneous Electrical "
        "Nerve Stimulator (TENS) trial end date."),
    "N345": ("Date range not valid with units submitted."),
    "N346": ("Missing/incomplete/invalid oral cavity designation "
        "code."),
    "N347": ("Your claim for a referred or purchased service cannot be "
        "paid because payment has already been made for this same service "
        "to another provider by a payment contractor representing the "
        "payer."),
    "N348": ("You chose that this service/supply/drug would be "
        "rendered/supplied and billed by a different "
        "practitioner/supplier."),
    "N349": ("The administration method and drug must be reported to "
        "adjudicate this service."),
    "N350": ("Missing/incomplete/invalid description of service for a "
        "Not Otherwise Classified (NOC) code or for an Unlisted/By Report "
        "procedure."),
    "N351": ("Service date outside of the approved treatment plan "
        "service dates."),
    "N352": ("Alert: There are no scheduled payments for this service. "
        "Submit a claim for each patient visit."),
    "N353": ("Alert: Benefits have been estimated, when the actual "
        "services have been rendered, additional payment will be considered "
        "based on the submitted claim."),
    "N354": ("Incomplete/invalid invoice"),
    "N355": ("Alert: The law permits exceptions to the refund "
        "requirement in two cases: - If you did not know, and could not "
        "have reasonably been expected to know, that we would not pay for "
        "this service; or - If you notified the patient in writing before "
        "providing the service that you believed that we were likely to "
        "deny the service, and the patient signed a statement agreeing to "
        "pay for the service.\n\nIf you come within either exception, or if "
        "you believe the carrier was wrong in its determination that we do "
        "not pay for this service, you should request appeal of this "
        "determination within 30 days of the date of this notice. Your "
        "request for review should include any additional information "
        "necessary to support your position.\n\nIf you request an appeal "
        "within 30 days of receiving this notice, you may delay refunding "
        "the amount to the patient until you receive the results of the "
        "review. If the review decision is favorable to you, you do not "
        "need to make any refund. If, however, the review is unfavorable, "
        "the law specifies that you must make the refund within 15 days of "
        "receiving the unfavorable review decision.\n\nThe law also permits "
        "you to request an appeal at any time within 120 days of the date "
        "you receive this notice. However, an appeal request that is "
        "received more than 30 days after the date of this notice, does not "
        "permit you to delay making the refund. Regardless of when a review "
        "is requested, the patient will be notified that you have requested "
        "one, and will receive a copy of the determination.\n\nThe patient "
        "has received a separate notice of this denial decision. The notice "
        "advises that he/she may be entitled to a refund of any amounts "
        "paid, if you should have known that we would not pay and did not "
        "tell him/her. It also instructs the patient to contact our office "
        "if he/she does not hear anything about a refund within 30 days"),
    "N356": ("Not covered when performed with, or subsequent to, a "
        "non-covered service."),
    "N357": ("Time frame requirements between this "
        "service/procedure/supply and a related service/procedure/supply "
        "have not been met."),
    "N358": ("Alert: This decision may be reviewed if additional "
        "documentation as described in the contract or plan benefit "
        "documents is submitted."),
    "N359": ("Missing/incomplete/invalid height."),
    "N360": ("Alert: Coordination of benefits has not been calculated "
        "when estimating benefits for this pre-determination. Submit "
        "payment information from the primary payer with the secondary "
        "claim."),
    "N362": ("The number of Days or Units of Service exceeds our "
        "acceptable maximum."),
    "N363": ("Alert: in the near future we are implementing new "
        "policies/procedures that would affect this determination."),
    "N364": ("Alert: According to our agreement, you must waive the "
        "deductible and/or coinsurance amounts."),
    "N365": ("This procedure code is not payable. It is for "
        "reporting/information purposes only."),
    "N366": ("Requested information not provided. The claim will be "
        "reopened if the information previously requested is submitted "
        "within one year after the date of this denial notice."),
    "N367": ("Alert: The claim information has been forwarded to a "
        "Consumer Spending Account processor for review; for example, "
        "flexible spending account or health savings account."),
    "N368": ("You must appeal the determination of the previously "
        "adjudicated claim."),
    "N369": ("Alert: Although this claim has been processed, it is "
        "deficient according to state legislation/regulation."),
    "N370": ("Billing exceeds the rental months covered/approved by "
        "the payer."),
    "N371": ("Alert: title of this equipment must be transferred to "
        "the patient."),
    "N372": ("Only reasonable and necessary maintenance/service "
        "charges are covered."),
    "N373": ("It has been determined that another payer paid the "
        "services as primary when they were not the primary payer. "
        "Therefore, we are refunding to the payer that paid as primary on "
        "your behalf."),
    "N374": ("Primary Medicare Part A insurance has been exhausted and "
        "a Part B Remittance Advice is required."),
    "N375": ("Missing/incomplete/invalid questionnaire/information "
        "required to determine dependent eligibility."),
    "N376": ("Subscriber/patient is assigned to active military duty, "
        "therefore primary coverage may be TRICARE."),
    "N377": ("Payment based on a processed replacement claim."),
    "N378": ("Missing/incomplete/invalid prescription quantity."),
    "N379": ("Claim level information does not match line level "
        "information."),
    "N380": ("The original claim has been processed, submit a "
        "corrected claim."),
    "N381": ("Consult our contractual agreement for "
        "restrictions/billing/payment information related to these "
        "charges."),
    "N382": ("Missing/incomplete/invalid patient identifier."),
    "N383": ("Not covered when deemed cosmetic."),
    "N384": ("Records indicate that the referenced body part/tooth has "
        "been removed in a previous procedure."),
    "N385": ("Notification of admission was not timely according to "
        "published plan procedures."),
    "N386": ("This decision was based on a National Coverage "
        "Determination (NCD). An NCD provides a coverage determination as "
        "to whether a particular item or service is covered. A copy of this "
        "policy is available at www.cms.gov/mcd/search.asp. If you do not "
        "have web access, you may contact the contractor to request a copy "
        "of the NCD."),
    "N387": ("Alert: Submit this claim to the patient's other insurer "
        "for potential payment of supplemental benefits. We did not forward "
        "the claim information."),
    "N388": ("Missing/incomplete/invalid prescription number"),
    "N389": ("Duplicate prescription number submitted."),
    "N390": ("This service/report cannot be billed separately."),
    "N391": ("Missing emergency department records."),
    "N392": ("Incomplete/invalid emergency department records."),
    "N393": ("Missing progress notes/report."),
    "N394": ("Incomplete/invalid progress notes/report."),
    "N395": ("Missing laboratory report."),
    "N396": ("Incomplete/invalid laboratory report."),
    "N397": ("Benefits are not available for incomplete "
        "service(s)/undelivered item(s)."),
    "N398": ("Missing elective consent form."),
    "N399": ("Incomplete/invalid elective consent form."),
    "N400": ("Alert: Electronically enabled providers should submit "
        "claims electronically."),
    "N401": ("Missing periodontal charting."),
    "N402": ("Incomplete/invalid periodontal charting."),
    "N403": ("Missing facility certification."),
    "N404": ("Incomplete/invalid facility certification."),
    "N405": ("This service is only covered when the donor's insurer(s) "
        "do not provide coverage for the service."),
    "N406": ("This service is only covered when the recipient's "
        "insurer(s) do not provide coverage for the service."),
    "N407": ("You are not an approved submitter for this transmission "
        "format."),
    "N408": ("This payer does not cover deductibles assessed by a "
        "previous payer."),
    "N409": ("This service is related to an accidental injury and is "
        "not covered unless provided within a specific time frame from the "
        "date of the accident."),
    "N410": ("Not covered unless the prescription changes."),
    "N418": ("Misrouted claim. See the payer's claim submission "
        "instructions."),
    "N419": ("Claim payment was the result of a payer's retroactive "
        "adjustment due to a retroactive rate change."),
    "N420": ("Claim payment was the result of a payer's retroactive "
        "adjustment due to a Coordination of Benefits or Third Party "
        "Liability Recovery."),
    "N421": ("Claim payment was the result of a payer's retroactive "
        "adjustment due to a review organization decision."),
    "N422": ("Claim payment was the result of a payer's retroactive "
        "adjustment due to a payer's contract incentive program."),
    "N423": ("Claim payment was the result of a payer's retroactive "
        "adjustment due to a non standard program."),
    "N424": ("Patient does not reside in the geographic area required "
        "for this type of payment."),
    "N425": ("Statutorily excluded service(s)."),
    "N426": ("No coverage when self-administered."),
    "N427": ("Payment for eyeglasses or contact lenses can be made "
        "only after cataract surgery."),
    "N428": ("Not covered when performed in this place of service."),
    "N429": ("Not covered when considered routine."),
    "N430": ("Procedure code is inconsistent with the units billed."),
    "N431": ("Not covered with this procedure."),
    "N432": ("Adjustment based on a Recovery Audit."),
    "N433": ("Resubmit this claim using only your National Provider "
        "Identifier (NPI)"),
    "N434": ("Missing/Incomplete/Invalid Present on Admission "
        "indicator."),
    "N435": ("Exceeds number/frequency approved /allowed within time "
        "period without support documentation."),
    "N436": ("The injury claim has not been accepted and a mandatory "
        "medical reimbursement has been made."),
    "N437": ("Alert: If the injury claim is accepted, these charges "
        "will be reconsidered."),
    "N438": ("This jurisdiction only accepts paper claims"),
    "N439": ("Missing anesthesia physical status report/indicators."),
    "N440": ("Incomplete/invalid anesthesia physical status "
        "report/indicators."),
    "N441": ("This missed appointment is not covered."),
    "N442": ("Payment based on an alternate fee schedule."),
    "N443": ("Missing/incomplete/invalid total time or begin/end "
        "time."),
    "N444": ("Alert: This facility has not filed the Election for High "
        "Cost Outlier form with the Division of Workers' Compensation."),
    "N445": ("Missing document for actual cost or paid amount."),
    "N446": ("Incomplete/invalid document for actual cost or paid "
        "amount."),
    "N447": ("Payment is based on a generic equivalent as required "
        "documentation was not provided."),
    "N448": ("This drug/service/supply is not included in the fee "
        "schedule or contracted/legislated fee arrangement"),
    "N449": ("Payment based on a comparable drug/service/supply."),
    "N450": ("Covered only when performed by the primary treating "
        "physician or the designee."),
    "N451": ("Missing Admission Summary Report."),
    "N452": ("Incomplete/invalid Admission Summary Report."),
    "N453": ("Missing Consultation Report."),
    "N454": ("Incomplete/invalid Consultation Report."),
    "N455": ("Missing Physician Order."),
    "N456": ("Incomplete/invalid Physician Order."),
    "N457": ("Missing Diagnostic Report."),
    "N458": ("Incomplete/invalid Diagnostic Report."),
    "N459": ("Missing Discharge Summary."),
    "N460": ("Incomplete/invalid Discharge Summary."),
    "N461": ("Missing Nursing Notes."),
    "N462": ("Incomplete/invalid Nursing Notes."),
    "N463": ("Missing support data for claim."),
    "N464": ("Incomplete/invalid support data for claim."),
    "N465": ("Missing Physical Therapy Notes/Report."),
    "N466": ("Incomplete/invalid Physical Therapy Notes/Report."),
    "N467": ("Missing Report of Tests and Analysis Report."),
    "N468": ("Incomplete/invalid Report of Tests and Analysis "
        "Report."),
    "N469": ("Alert: Claim/Service(s) subject to appeal process, see "
        "section 935 of Medicare Prescription Drug, Improvement, and "
        "Modernization Act of 2003 (MMA)."),
    "N470": ("This payment will complete the mandatory medical "
        "reimbursement limit."),
    "N471": ("Missing/incomplete/invalid HIPPS Rate Code."),
    "N472": ("Payment for this service has been issued to another "
        "provider."),
    "N473": ("Missing certification."),
    "N474": ("Incomplete/invalid certification"),
    "N475": ("Missing completed referral form."),
    "N476": ("Incomplete/invalid completed referral form"),
    "N477": ("Missing Dental Models."),
    "N478": ("Incomplete/invalid Dental Models"),
    "N479": ("Missing Explanation of Benefits (Coordination of "
        "Benefits or Medicare Secondary Payer)."),
    "N480": ("Incomplete/invalid Explanation of Benefits (Coordination "
        "of Benefits or Medicare Secondary Payer)."),
    "N481": ("Missing Models."),
    "N482": ("Incomplete/invalid Models"),
    "N483": ("Missing Periodontal Charts."),
    "N484": ("Incomplete/invalid Periodontal Charts"),
    "N485": ("Missing Physical Therapy Certification."),
    "N486": ("Incomplete/invalid Physical Therapy Certification."),
    "N487": ("Missing Prosthetics or Orthotics Certification."),
    "N488": ("Incomplete/invalid Prosthetics or Orthotics "
        "Certification"),
    "N489": ("Missing referral form."),
    "N490": ("Incomplete/invalid referral form"),
    "N491": ("Missing/Incomplete/Invalid Exclusionary Rider "
        "Condition."),
    "N492": ("Alert: A network provider may bill the member for this "
        "service if the member requested the service and agreed in writing, "
        "prior to receiving the service, to be financially responsible for "
        "the billed charge."),
    "N493": ("Missing Doctor First Report of Injury."),
    "N494": ("Incomplete/invalid Doctor First Report of Injury."),
    "N495": ("Missing Supplemental Medical Report."),
    "N496": ("Incomplete/invalid Supplemental Medical Report."),
    "N497": ("Missing Medical Permanent Impairment or Disability "
        "Report."),
    "N498": ("Incomplete/invalid Medical Permanent Impairment or "
        "Disability Report."),
    "N499": ("Missing Medical Legal Report."),
    "N500": ("Incomplete/invalid Medical Legal Report."),
    "N501": ("Missing Vocational Report."),
    "N502": ("Incomplete/invalid Vocational Report."),
    "N503": ("Missing Work Status Report."),
    "N504": ("Incomplete/invalid Work Status Report."),
    "N505": ("Alert: This response includes only services that could "
        "be estimated in real time. No estimate will be provided for the "
        "services that could not be estimated in real time."),
    "N506": ("Alert: This is an estimate of the member's liability "
        "based on the information available at the time the estimate was "
        "processed. Actual coverage and member liability amounts will be "
        "determined when the claim is processed. This is not a "
        "pre-authorization or a guarantee of payment."),
    "N507": ("Plan distance requirements have not been met."),
    "N508": ("Alert: This real time claim adjudication response "
        "represents the member responsibility to the provider for services "
        "reported. The member will receive an Explanation of Benefits "
        "electronically or in the mail. Contact the insurer if there are "
        "any questions."),
    "N509": ("Alert: A current inquiry shows the member's Consumer "
        "Spending Account contains sufficient funds to cover the member "
        "liability for this claim/service. Actual payment from the Consumer "
        "Spending Account will depend on the availability of funds and "
        "determination of eligible services at the time of payment "
        "processing."),
    "N510": ("Alert: A current inquiry shows the member's Consumer "
        "Spending Account does not contain sufficient funds to cover the "
        "member's liability for this claim/service. Actual payment from the "
        "Consumer Spending Account will depend on the availability of funds "
        "and determination of eligible services at the time of payment "
        "processing."),
    "N511": ("Alert: Information on the availability of Consumer "
        "Spending Account funds to cover the member liability on this "
        "claim/service is not available at this time."),
    "N512": ("Alert: This is the initial remit of a non-NCPDP claim "
        "originally submitted real-time without change to the "
        "adjudication."),
    "N513": ("Alert: This is the initial remit of a non-NCPDP claim "
        "originally submitted real-time with a change to the "
        "adjudication."),
    "N516": ("Records indicate a mismatch between the submitted NPI "
        "and EIN."),
    "N517": ("Resubmit a new claim with the requested information."),
    "N518": ("No separate payment for accessories when furnished for "
        "use with oxygen equipment."),
    "N519": ("Invalid combination of HCPCS modifiers."),
    "N520": ("Alert: Payment made from a Consumer Spending Account."),
    "N521": ("Mismatch between the submitted provider information and "
        "the provider information stored in our system."),
    "N522": ("Duplicate of a claim processed, or to be processed, as a "
        "crossover claim."),
    "N523": ("The limitation on outlier payments defined by this payer "
        "for this service period has been met. The outlier payment "
        "otherwise applicable to this claim has not been paid."),
    "N524": ("Based on policy this payment constitutes payment in "
        "full."),
    "N525": ("These services are not covered when performed within the "
        "global period of another service."),
    "N526": ("Not qualified for recovery based on employer size."),
    "N527": ("We processed this claim as the primary payer prior to "
        "receiving the recovery demand."),
    "N528": ("Patient is entitled to benefits for Institutional "
        "Services only."),
    "N529": ("Patient is entitled to benefits for Professional "
        "Services only."),
    "N530": ("Not Qualified for Recovery based on enrollment "
        "information."),
    "N531": ("Not qualified for recovery based on direct payment of "
        "premium."),
    "N532": ("Not qualified for recovery based on disability and "
        "working status."),
    "N533": ("Services performed in an Indian Health Services facility "
        "under a self-insured tribal Group Health Plan."),
    "N534": ("This is an individual policy, the employer does not "
        "participate in plan sponsorship."),
    "N535": ("Payment is adjusted when procedure is performed in this "
        "place of service based on the submitted procedure code and place "
        "of service."),
    "N536": ("We are not changing the prior payer's determination of "
        "patient responsibility, which you may collect, as this service is "
        "not covered by us."),
    "N537": ("We have examined claims history and no records of the "
        "services have been found."),
    "N538": ("A facility is responsible for payment to outside "
        "providers who furnish these services/supplies/drugs to its "
        "patients/residents."),
    "N539": ("Alert: We processed appeals/waiver requests on your "
        "behalf and that request has been denied."),
    "N540": ("Payment adjusted based on the interrupted stay "
        "policy."),
    "N541": ("Mismatch between the submitted insurance type code and "
        "the information stored in our system."),
    "N542": ("Missing income verification."),
    "N543": ("Incomplete/invalid income verification"),
    "N544": ("Alert: Although this was paid, you have billed with a "
        "referring/ordering provider that does not match our system record. "
        "Unless, corrected, this will not be paid in the future."),
    "N545": ("Payment reduced based on status as an unsuccessful "
        "eprescriber per the Electronic Prescribing (eRx) Incentive "
        "Program."),
    "N546": ("Payment represents a previous reduction based on the "
        "Electronic Prescribing (eRx) Incentive Program."),
    "N547": ("A refund request (Frequency Type Code 8) was processed "
        "previously."),
    "N548": ("Alert: Patient's calendar year deductible has been "
        "met."),
    "N549": ("Alert: Patient's calendar year out-of-pocket maximum has "
        "been met."),
    "N550": ("Alert: You have not responded to requests to revalidate "
        "your provider/supplier enrollment information. Your failure to "
        "revalidate your enrollment information will result in a payment "
        "hold in the near future."),
    "N551": ("Payment adjusted based on the Ambulatory Surgical Center "
        "(ASC) Quality Reporting Program."),
    "N552": ("Payment adjusted to reverse a previous withhold/bonus "
        "amount."),
    "N553": ("Payment adjusted based on a Low Income Subsidy (LIS) "
        "retroactive coverage or status change."),
}

claim_adjustment_reasons = {
    "1": "Deductible Amount",
    "2": "Coinsurance Amount",
    "3": "Co-payment Amount",
    "4": "The procedure code is inconsistent with the modifier used or " \
        "a required modifier is missing. Note: Refer to the 835 Healthcare " \
        "Policy Identification Segment (loop 2110 Service Payment " \
        "Information REF), if present.",
    "5": "The procedure code/bill type is inconsistent with the place " \
        "of service. Note: Refer to the 835 Healthcare Policy " \
        "Identification Segment (loop 2110 Service Payment Information " \
        "REF), if present.",
    "6": "The procedure/revenue code is inconsistent with the " \
        "patient's age. Note: Refer to the 835 Healthcare Policy " \
        "Identification Segment (loop 2110 Service Payment Information " \
        "REF), if present.",
    "7": "The procedure/revenue code is inconsistent with the " \
        "patient's gender. Note: Refer to the 835 Healthcare Policy " \
        "Identification Segment (loop 2110 Service Payment Information " \
        "REF), if present.",
    "8": "The procedure code is inconsistent with the provider " \
        "type/specialty (taxonomy). Note: Refer to the 835 Healthcare " \
        "Policy Identification Segment (loop 2110 Service Payment " \
        "Information REF), if present.",
    "9": "The diagnosis is inconsistent with the patient's age. Note: " \
        "Refer to the 835 Healthcare Policy Identification Segment " \
        "(loop 2110 Service Payment Information REF), if present.",
    "10": "The diagnosis is inconsistent with the patient's gender. " \
        "Note: Refer to the 835 Healthcare Policy Identification Segment " \
        "(loop 2110 Service Payment Information REF), if present.",
    "11": "The diagnosis is inconsistent with the procedure. Note: " \
        "Refer to the 835 Healthcare Policy Identification Segment " \
        "(loop 2110 Service Payment Information REF), if present.",
    "12": "The diagnosis is inconsistent with the provider type. Note: " \
        "Refer to the 835 Healthcare Policy Identification Segment " \
        "(loop 2110 Service Payment Information REF), if present.",
    "13": "The date of death precedes the date of service.",
    "14": "The date of birth follows the date of service.",
    "15": "The authorization number is missing, invalid, or does not " \
        "apply to the billed services or provider.",
    "16": "Claim/service lacks information which is needed for " \
        "adjudication. At least one Remark Code must be provided (may be " \
        "comprised of either the NCPDP Reject Reason Code, or " \
        "Remittance Advice Remark Code that is not an ALERT.)",
    "18": "Duplicate claim/service. This change effective 1/1/2013: " \
        "Exact duplicate claim/service (Use with Group Code OA).",
    "19": "This is a work-related injury/illness and thus the " \
        "liability of the Worker's Compensation Carrier.",
    "20": "This injury/illness is covered by the liability carrier.",
    "21": "This injury/illness is the liability of the no-fault " \
        "carrier.",
    "22": "This care may be covered by another payer per coordination " \
        "of benefits.",
    "23": "The impact of prior payer(s) adjudication including " \
        "payments and/or adjustments.",
    "24": "Charges are covered under a capitation agreement/managed " \
        "care plan.",
    "26": "Expenses incurred prior to coverage.",
    "27": "Expenses incurred after coverage terminated.",
    "29": "The time limit for filing has expired.",
    "31": "Patient cannot be identified as our insured.",
    "32": "Our records indicate that this dependent is not an eligible " \
        "dependent as defined.",
    "33": "Insured has no dependent coverage.",
    "34": "Insured has no coverage for newborns.",
    "35": "Lifetime benefit maximum has been reached.",
    "38": "Services not provided or authorized by designated " \
        "(network/primary care) providers.",
    "39": "Services denied at the time authorization/pre-certification " \
        "was requested.",
    "40": "Charges do not meet qualifications for emergent/urgent " \
        "care. Note: Refer to the 835 Healthcare Policy Identification " \
        "Segment (loop 2110 Service Payment Information REF), if present.",
    "44": "Prompt-pay discount.",
    "45": "Charge exceeds fee schedule/maximum allowable or " \
        "contracted/legislated fee arrangement. (Use Group Codes PR or CO " \
        "depending upon liability).",
    "49": "These are non-covered services because this is a routine " \
        "exam or screening procedure done in conjunction with a routine " \
        "exam. Note: Refer to the 835 Healthcare Policy Identification " \
        "Segment (loop 2110 Service Payment Information REF), if present.",
    "50": "These are non-covered services because this is not deemed a " \
        "'medical necessity' by the payer. Note: Refer to the 835 " \
        "Healthcare Policy Identification Segment (loop 2110 Service " \
        "Payment Information REF), if present.",
    "51": "These are non-covered services because this is a " \
        "pre-existing condition. Note: Refer to the 835 Healthcare Policy " \
        "Identification Segment (loop 2110 Service Payment Information " \
        "REF), if present.",
    "53": "Services by an immediate relative or a member of the same " \
        "household are not covered.",
    "54": "Multiple physicians/assistants are not covered in this " \
        "case. Note: Refer to the 835 Healthcare Policy Identification " \
        "Segment (loop 2110 Service Payment Information REF), if present.",
    "55": "Procedure/treatment is deemed experimental/investigational " \
        "by the payer. Note: Refer to the 835 Healthcare Policy " \
        "Identification Segment (loop 2110 Service Payment Information " \
        "REF), if present.",
    "56": "Procedure/treatment has not been deemed 'proven to be " \
        "effective' by the payer. Note: Refer to the 835 Healthcare Policy " \
        "Identification Segment (loop 2110 Service Payment Information " \
        "REF), if present.",
    "58": "Treatment was deemed by the payer to have been rendered in " \
        "an inappropriate or invalid place of service. Note: Refer to the " \
        "835 Healthcare Policy Identification Segment (loop 2110 Service " \
        "Payment Information REF), if present.",
    "59": "Processed based on multiple or concurrent procedure rules. " \
        "(For example multiple surgery or diagnostic imaging, concurrent " \
        "anesthesia.) Note: Refer to the 835 Healthcare Policy " \
        "Identification Segment (loop 2110 Service Payment Information " \
        "REF), if present.",
    "60": "Charges for outpatient services are not covered when " \
        "performed within a period of time prior to or after inpatient " \
        "services.",
    "61": "Penalty for failure to obtain second surgical opinion. " \
        "Note: Refer to the 835 Healthcare Policy Identification Segment " \
        "(loop 2110 Service Payment Information REF), if present.",
    "66": "Blood Deductible.",
    "69": "Day outlier amount.",
    "70": "Cost outlier - Adjustment to compensate for additional " \
        "costs.",
    "74": "Indirect Medical Education Adjustment.",
    "75": "Direct Medical Education Adjustment.",
    "76": "Disproportionate Share Adjustment.",
    "78": "Non-Covered days/Room charge adjustment.",
    "85": "Patient Interest Adjustment (Use Only Group code PR) Notes: " \
        "Only use when the payment of interest is the responsibility of the " \
        "patient.",
    "89": "Professional fees removed from charges.",
    "90": "Ingredient cost adjustment. Note: To be used for " \
        "pharmaceuticals only.",
    "91": "Dispensing fee adjustment.",
    "94": "Processed in Excess of charges.",
    "95": "Plan procedures not followed.",
    "96": "Non-covered charge(s). At least one Remark Code must be " \
        "provided (may be comprised of either the NCPDP Reject Reason Code, " \
        "or Remittance Advice Remark Code that is not an ALERT.) Note: " \
        "Refer to the 835 Healthcare Policy Identification Segment (loop " \
        "2110 Service Payment Information REF), if present.",
    "97": "The benefit for this service is included in the " \
        "payment/allowance for another service/procedure that has already " \
        "been adjudicated. Note: Refer to the 835 Healthcare Policy " \
        "Identification Segment (loop 2110 Service Payment Information " \
        "REF), if present.",
    "100": "Payment made to patient/insured/responsible " \
        "party/employer.",
    "101": "Predetermination: anticipated payment upon completion of " \
        "services or claim adjudication.",
    "102": "Major Medical Adjustment.",
    "103": "Provider promotional discount (e.g., Senior citizen " \
        "discount).",
    "104": "Managed care withholding.",
    "105": "Tax withholding.",
    "106": "Patient payment option/election not in effect.",
    "107": "The related or qualifying claim/service was not identified " \
        "on this claim. Note: Refer to the 835 Healthcare Policy " \
        "Identification Segment (loop 2110 Service Payment Information " \
        "REF), if present.",
    "108": "Rent/purchase guidelines were not met. Note: Refer to the " \
        "835 Healthcare Policy Identification Segment (loop 2110 Service " \
        "Payment Information REF), if present.",
    "109": "Claim not covered by this payer/contractor. You must send " \
        "the claim to the correct payer/contractor. This change effective " \
        "11/1/2012: Claim/service not covered by this payer/contractor. You " \
        "must send the claim/service to the correct payer/contractor.",
    "110": "Billing date predates service date.",
    "111": "Not covered unless the provider accepts assignment.",
    "112": "Service not furnished directly to the patient and/or not " \
        "documented.",
    "114": "Procedure/product not approved by the Food and Drug " \
        "Administration.",
    "115": "Procedure postponed, canceled, or delayed.",
    "116": "The advance indemnification notice signed by the patient " \
        "did not comply with requirements.",
    "117": "Transportation is only covered to the closest facility " \
        "that can provide the necessary care.",
    "118": "ESRD network support adjustment.",
    "119": "Benefit maximum for this time period or occurrence has " \
        "been reached.",
    "121": "Indemnification adjustment - compensation for outstanding " \
        "member responsibility.",
    "122": "Psychiatric reduction.",
    "125": "Submission/billing error(s). At least one Remark Code must " \
        "be provided (may be comprised of either the NCPDP Reject Reason " \
        "Code, or Remittance Advice Remark Code that is not an ALERT.)",
    "128": "Newborn's services are covered in the mother's " \
        "Allowance.",
    "129": "Prior processing information appears incorrect. At least " \
        "one Remark Code must be provided (may be comprised of either the " \
        "NCPDP Reject Reason Code, or Remittance Advice Remark Code that is " \
        "not an ALERT.)",
    "130": "Claim submission fee.",
    "131": "Claim specific negotiated discount.",
    "132": "Prearranged demonstration project adjustment.",
    "133": "The disposition of this claim/service is pending further " \
        "review.",
    "134": "Technical fees removed from charges.",
    "135": "Interim bills cannot be processed.",
    "136": "Failure to follow prior payer's coverage rules. (Use Group " \
        "Code OA).",
    "137": "Regulatory Surcharges, Assessments, Allowances or Health " \
        "Related Taxes.",
    "138": "Appeal procedures not followed or time limits not met.",
    "139": "Contracted funding agreement - Subscriber is employed by " \
        "the provider of services.",
    "140": "Patient/Insured health identification number and name do " \
        "not match.",
    "141": "Claim spans eligible and ineligible periods of coverage.",
    "142": "Monthly Medicaid patient liability amount.",
    "143": "Portion of payment deferred.",
    "144": "Incentive adjustment, e.g. preferred product/service.",
    "146": "Diagnosis was invalid for the date(s) of service " \
        "reported.",
    "147": "Provider contracted/negotiated rate expired or not on " \
        "file.",
    "148": "Information from another provider was not provided or was " \
        "insufficient/incomplete. At least one Remark Code must be provided " \
        "(may be comprised of either the NCPDP Reject Reason Code, or " \
        "Remittance Advice Remark Code that is not an ALERT.)",
    "149": "Lifetime benefit maximum has been reached for this " \
        "service/benefit category.",
    "150": "Payer deems the information submitted does not support " \
        "this level of service.",
    "151": "Payment adjusted because the payer deems the information " \
        "submitted does not support this many/frequency of services.",
    "152": "Payer deems the information submitted does not support " \
        "this length of service. Note: Refer to the 835 Healthcare Policy " \
        "Identification Segment (loop 2110 Service Payment Information " \
        "REF), if present.",
    "153": "Payer deems the information submitted does not support " \
        "this dosage.",
    "154": "Payer deems the information submitted does not support " \
        "this day's supply.",
    "155": "Patient refused the service/procedure.",
    "157": "Service/procedure was provided as a result of an act of " \
        "war.",
    "158": "Service/procedure was provided outside of the United " \
        "States.",
    "159": "Service/procedure was provided as a result of terrorism.",
    "160": "Injury/illness was the result of an activity that is a " \
        "benefit exclusion.",
    "161": "Provider performance bonus",
    "162": "State-mandated Requirement for Property and Casualty, see " \
        "Claim Payment Remarks Code for specific explanation.",
    "163": "Attachment referenced on the claim was not received.",
    "164": "Attachment referenced on the claim was not received in a " \
        "timely fashion.",
    "165": "Referral absent or exceeded.",
    "166": "These services were submitted after this payers " \
        "responsibility for processing claims under this plan ended.",
    "167": "This (these) diagnosis(es) is (are) not covered. Note: " \
        "Refer to the 835 Healthcare Policy Identification Segment (loop " \
        "2110 Service Payment Information REF), if present.",
    "168": "Service(s) have been considered under the patient's " \
        "medical plan. Benefits are not available under this dental plan.",
    "169": "Alternate benefit has been provided.",
    "170": "Payment is denied when performed/billed by this type of " \
        "provider. Note: Refer to the 835 Healthcare Policy Identification " \
        "Segment (loop 2110 Service Payment Information REF), if present.",
    "171": "Payment is denied when performed/billed by this type of " \
        "provider in this type of facility. Note: Refer to the 835 " \
        "Healthcare Policy Identification Segment (loop 2110 Service " \
        "Payment Information REF), if present.",
    "172": "Payment is adjusted when performed/billed by a provider of " \
        "this specialty. Note: Refer to the 835 Healthcare Policy " \
        "Identification Segment (loop 2110 Service Payment Information " \
        "REF), if present.",
    "173": "Service was not prescribed by a physician.",
    "174": "Service was not prescribed prior to delivery.",
    "175": "Prescription is incomplete.",
    "176": "Prescription is not current.",
    "177": "Patient has not met the required eligibility " \
        "requirements.",
    "178": "Patient has not met the required spend down " \
        "requirements.",
    "179": "Patient has not met the required waiting requirements. " \
        "Note: Refer to the 835 Healthcare Policy Identification Segment " \
        "(loop 2110 Service Payment Information REF), if present.",
    "180": "Patient has not met the required residency requirements.",
    "181": "Procedure code was invalid on the date of service.",
    "182": "Procedure modifier was invalid on the date of service.",
    "183": "The referring provider is not eligible to refer the " \
        "service billed. Note: Refer to the 835 Healthcare Policy " \
        "Identification Segment (loop 2110 Service Payment Information " \
        "REF), if present.",
    "184": "The prescribing/ordering provider is not eligible to " \
        "prescribe/order the service billed. Note: Refer to the 835 " \
        "Healthcare Policy Identification Segment (loop 2110 Service " \
        "Payment Information REF), if present.",
    "185": "The rendering provider is not eligible to perform the " \
        "service billed. Note: Refer to the 835 Healthcare Policy " \
        "Identification Segment (loop 2110 Service Payment Information " \
        "REF), if present.",
    "186": "Level of care change adjustment.",
    "187": "Consumer Spending Account payments (includes but is not " \
        "limited to Flexible Spending Account, Health Savings Account, " \
        "Health Reimbursement Account, etc.)",
    "188": "This product/procedure is only covered when used according " \
        "to FDA recommendations.",
    "189": "'Not otherwise classified' or 'unlisted' procedure code " \
        "(CPT/HCPCS) was billed when there is a specific procedure code for " \
        "this procedure/service",
    "190": "Payment is included in the allowance for a Skilled Nursing " \
        "Facility (SNF) qualified stay.",
    "191": "Not a work related injury/illness and thus not the " \
        "liability of the workers' compensation carrier Note: If adjustment " \
        "is at the Claim Level, the payer must send and the provider should " \
        "refer to the 835 Insurance Policy Number Segment (Loop 2100 Other " \
        "Claim Related Information REF qualifier 'IG') for the " \
        "jurisdictional regulation. If adjustment is at the Line Level, the " \
        "payer must send and the provider should refer to the 835 " \
        "Healthcare Policy Identification Segment (loop 2110 Service " \
        "Payment information REF)",
    "192": "Non standard adjustment code from paper remittance. Note: " \
        "This code is to be used by providers/payers providing Coordination " \
        "of Benefits information to another payer in the 837 transaction " \
        "only. This code is only used when the non-standard code cannot be " \
        "reasonably mapped to an existing Claims Adjustment Reason Code, " \
        "specifically Deductible, Coinsurance and Co-payment.",
    "193": "Original payment decision is being maintained. Upon " \
        "review, it was determined that this claim was processed " \
        "properly.",
    "194": "Anesthesia performed by the operating physician, the " \
        "assistant surgeon or the attending physician.",
    "195": "Refund issued to an erroneous priority payer for this " \
        "claim/service.",
    "197": "Precertification/authorization/notification absent.",
    "198": "Precertification/authorization exceeded.",
    "199": "Revenue code and Procedure code do not match.",
    "200": "Expenses incurred during lapse in coverage",
    "201": "Workers Compensation case settled. Patient is responsible " \
        "for amount of this claim/service through WC 'Medicare set aside " \
        "arrangement' or other agreement. (Use group code PR).",
    "202": "Non-covered personal comfort or convenience services.",
    "203": "Discontinued or reduced service.",
    "204": "This service/equipment/drug is not covered under the " \
        "patient's current benefit plan",
    "205": "Pharmacy discount card processing fee",
    "206": "National Provider Identifier - missing.",
    "207": "National Provider identifier - Invalid format",
    "208": "National Provider Identifier - Not matched.",
    "209": "Per regulatory or other agreement. The provider cannot " \
        "collect this amount from the patient. However, this amount may be " \
        "billed to subsequent payer. Refund to patient if collected. (Use " \
        "Group code OA)",
    "210": "Payment adjusted because pre-certification/authorization " \
        "not received in a timely fashion",
    "211": "National Drug Codes (NDC) not eligible for rebate, are not " \
        "covered.",
    "212": "Administrative surcharges are not covered",
    "213": "Non-compliance with the physician self referral " \
        "prohibition legislation or payer policy.",
    "214": "Workers' Compensation claim adjudicated as " \
        "non-compensable. This Payer not liable for claim or " \
        "service/treatment. Note: If adjustment is at the Claim Level, the " \
        "payer must send and the provider should refer to the 835 Insurance " \
        "Policy Number Segment (Loop 2100 Other Claim Related Information " \
        "REF qualifier 'IG') for the jurisdictional regulation. If " \
        "adjustment is at the Line Level, the payer must send and the " \
        "provider should refer to the 835 Healthcare Policy Identification " \
        "Segment (loop 2110 Service Payment information REF). To be used " \
        "for Workers' Compensation only",
    "215": "Based on subrogation of a third party settlement",
    "216": "Based on the findings of a review organization",
    "217": "Based on payer reasonable and customary fees. No maximum " \
        "allowable defined by legislated fee arrangement. (Note: To be used " \
        "for Workers' Compensation only)",
    "218": "Based on entitlement to benefits. Note: If adjustment is " \
        "at the Claim Level, the payer must send and the provider should " \
        "refer to the 835 Insurance Policy Number Segment (Loop 2100 Other " \
        "Claim Related Information REF qualifier 'IG') for the " \
        "jurisdictional regulation. If adjustment is at the Line Level, the " \
        "payer must send and the provider should refer to the 835 " \
        "Healthcare Policy Identification Segment (loop 2110 Service " \
        "Payment information REF). To be used for Workers' Compensation " \
        "only",
    "219": "Based on extent of injury. Note: If adjustment is at the " \
        "Claim Level, the payer must send and the provider should refer to " \
        "the 835 Insurance Policy Number Segment (Loop 2100 Other Claim " \
        "Related Information REF qualifier 'IG') for the jurisdictional " \
        "regulation. If adjustment is at the Line Level, the payer must " \
        "send and the provider should refer to the 835 Healthcare Policy " \
        "Identification Segment (loop 2110 Service Payment information " \
        "REF).",
    "220": "The applicable fee schedule does not contain the billed " \
        "code. Please resubmit a bill with the appropriate fee schedule " \
        "code(s) that best describe the service(s) provided and supporting " \
        "documentation if required. (Note: To be used for Workers' " \
        "Compensation only)",
    "221": "Workers' Compensation claim is under investigation. Note: " \
        "If adjustment is at the Claim Level, the payer must send and the " \
        "provider should refer to the 835 Insurance Policy Number Segment " \
        "(Loop 2100 Other Claim Related Information REF qualifier 'IG') for " \
        "the jurisdictional regulation. If adjustment is at the Line Level, " \
        "the payer must send and the provider should refer to the 835 " \
        "Healthcare Policy Identification Segment (loop 2110 Service " \
        "Payment information REF).",
    "222": "Exceeds the contracted maximum number of hours/days/units " \
        "by this provider for this period. This is not patient specific. " \
        "Note: Refer to the 835 Healthcare Policy Identification Segment " \
        "(loop 2110 Service Payment Information REF), if present.",
    "223": "Adjustment code for mandated federal, state or local " \
        "law/regulation that is not already covered by another code and is " \
        "mandated before a new code can be created.",
    "224": "Patient identification compromised by identity theft. " \
        "Identity verification required for processing this and future " \
        "claims.",
    "225": "Penalty or Interest Payment by Payer (Only used for plan " \
        "to plan encounter reporting within the 837)",
    "226": "Information requested from the Billing/Rendering Provider " \
        "was not provided or was insufficient/incomplete. At least one " \
        "Remark Code must be provided (may be comprised of either the NCPDP " \
        "Reject Reason Code, or Remittance Advice Remark Code that is not " \
        "an ALERT.)",
    "227": "Information requested from the patient/insured/responsible " \
        "party was not provided or was insufficient/incomplete. At least " \
        "one Remark Code must be provided (may be comprised of either the " \
        "NCPDP Reject Reason Code, or Remittance Advice Remark Code that is " \
        "not an ALERT.)",
    "228": "Denied for failure of this provider, another provider or " \
        "the subscriber to supply requested information to a previous payer " \
        "for their adjudication",
    "229": "Partial charge amount not considered by Medicare due to " \
        "the initial claim Type of Bill being 12X. Note: This code can only " \
        "be used in the 837 transaction to convey Coordination of Benefits " \
        "information when the secondary payer's cost avoidance policy " \
        "allows providers to bypass claim submission to a prior payer. Use " \
        "Group Code PR.",
    "230": "No available or correlating CPT/HCPCS code to describe " \
        "this service. Note: Used only by Property and Casualty.",
    "231": "Mutually exclusive procedures cannot be done in the same " \
        "day/setting. Note: Refer to the 835 Healthcare Policy " \
        "Identification Segment (loop 2110 Service Payment Information " \
        "REF), if present.",
    "232": "Institutional Transfer Amount. Note - Applies to " \
        "institutional claims only and explains the DRG amount difference " \
        "when the patient care crosses multiple institutions.",
    "233": "Services/charges related to the treatment of a " \
        "hospital-acquired condition or preventable medical error.",
    "234": "This procedure is not paid separately. At least one Remark " \
        "Code must be provided (may be comprised of either the NCPDP Reject " \
        "Reason Code, or Remittance Advice Remark Code that is not an " \
        "ALERT.)",
    "235": "Sales Tax",
    "236": "This procedure or procedure/modifier combination is not " \
        "compatible with another procedure or procedure/modifier " \
        "combination provided on the same day according to the National " \
        "Correct Coding Initiative.",
    "237": "Legislated/Regulatory Penalty. At least one Remark Code " \
        "must be provided (may be comprised of either the NCPDP Reject " \
        "Reason Code, or Remittance Advice Remark Code that is not an " \
        "ALERT.)",
    "238": "Claim spans eligible and ineligible periods of coverage, " \
        "this is the reduction for the ineligible period (use Group Code " \
        "PR).",
    "239": "Claim spans eligible and ineligible periods of coverage. " \
        "Rebill separate claims (use Group Code OA). This change effective " \
        "11/1/2012: Claim spans eligible and ineligible periods of " \
        "coverage. Rebill separate claims.",
    "A0": "Patient refund amount.",
    "A1": "Claim/Service denied. At least one Remark Code must be " \
        "provided (may be comprised of either the NCPDP Reject Reason Code, " \
        "or Remittance Advice Remark Code that is not an ALERT.)",
    "A5": "Medicare Claim PPS Capital Cost Outlier Amount.",
    "A6": "Prior hospitalization or 30 day transfer requirement not " \
        "met.",
    "A7": "Presumptive Payment Adjustment",
    "A8": "Ungroupable DRG.",
    "B1": "Non-covered visits.",
    "B4": "Late filing penalty.",
    "B5": "Coverage/program guidelines were not met or were " \
        "exceeded.",
    "B7": "This provider was not certified/eligible to be paid for " \
        "this procedure/service on this date of service. Note: Refer to the " \
        "835 Healthcare Policy Identification Segment (loop 2110 Service " \
        "Payment Information REF), if present.",
    "B8": "Alternative services were available, and should have been " \
        "utilized. Note: Refer to the 835 Healthcare Policy Identification " \
        "Segment (loop 2110 Service Payment Information REF), if present.",
    "B9": "Patient is enrolled in a Hospice.",
    "B10": "Allowed amount has been reduced because a component of the " \
        "basic procedure/test was paid. The beneficiary is not liable for " \
        "more than the charge limit for the basic procedure/test.",
    "B11": "The claim/service has been transferred to the proper " \
        "payer/processor for processing. Claim/service not covered by this " \
        "payer/processor.",
    "B12": "Services not documented in patients' medical records.",
    "B13": "Previously paid. Payment for this claim/service may have " \
        "been provided in a previous payment.",
    "B14": "Only one visit or consultation per physician per day is " \
        "covered.",
    "B15": "This service/procedure requires that a qualifying " \
        "service/procedure be received and covered. The qualifying other " \
        "service/procedure has not been received/adjudicated. Note: Refer " \
        "to the 835 Healthcare Policy Identification Segment (loop 2110 " \
        "Service Payment Information REF), if present.",
    "B16": "'New Patient' qualifications were not met.",
    "B20": "Procedure/service was partially or fully furnished by " \
        "another provider.",
    "B22": "This payment is adjusted based on the diagnosis.",
    "B23": "Procedure billed is not authorized per your Clinical " \
        "Laboratory Improvement Amendment (CLIA) proficiency test.",
    "W1": "Workers' compensation jurisdictional fee schedule " \
        "adjustment. Note: If adjustment is at the Claim Level, the payer " \
        "must send and the provider should refer to the 835 Class of " \
        "Contract Code Identification Segment (Loop 2100 Other Claim " \
        "Related Information REF). If adjustment is at the Line Level, the " \
        "payer must send and the provider should refer to the 835 " \
        "Healthcare Policy Identification Segment (loop 2110 Service " \
        "Payment information REF).",
    "W2": "Payment reduced or denied based on workers' compensation " \
        "jurisdictional regulations or payment policies, use only if no " \
        "other code is applicable. Note: If adjustment is at the Claim " \
        "Level, the payer must send and the provider should refer to the " \
        "835 Insurance Policy Number Segment (Loop 2100 Other Claim Related " \
        "Information REF qualifier 'IG') for the jurisdictional regulation. " \
        "If adjustment is at the Line Level, the payer must send and the " \
        "provider should refer to the 835 Healthcare Policy Identification " \
        "Segment (loop 2110 Service Payment information REF). To be used " \
        "for Workers' Compensation only.",
}
