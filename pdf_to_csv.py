import re

from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

def convert_pdf(path):

    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

    fp = file(path, 'rb')
    process_pdf(rsrcmgr, device, fp)
    fp.close()
    device.close()

    str = retstr.getvalue()
    retstr.close()
    return str

if __name__ == "__main__":
    pdf_text = convert_pdf("./dir98_extract.pdf")
    # p = re.compile("[A-Z][0-9]+")print re.findall("[A-Z][0-9]+.*?[A-Z][0-9]+", pdf_text, re.DOTALL)[1]
    # p = re.compile("[A-Z][0-9]+.*?[A-Z][0-9]+")
    # m = p.search(pdf_text)

    # print re.findall("[A-Z][0-9]+.*?[A-Z][0-9]+", pdf_text, re.DOTALL)
    # regex = "([A-Z][0-9]+)(.*?)(?=([A-Z][0-9]+))"
    # regex = "([A-Z][0-9]+)(.*?)(?=([A-Z][0-9]+))"
    regex = "([A-Z]\s?[0-9]+)(.*?)(?=([A-Z]\s?[0-9]+))"
    # regex = "[A-Z][0-9]+.*?[A-Z][0-9]+"
    # print re.findall(regex, pdf_text, re.DOTALL)[0]
    # print re.findall(regex, pdf_text, re.DOTALL)[1]
    # print re.findall(regex, pdf_text, re.DOTALL)[2]

    # print len(re.findall(regex, pdf_text, re.DOTALL)[0])
    for (cmpy_code, cmpy_desc, next_cmpy_code) in re.findall(regex, pdf_text, re.DOTALL):
    # for (cmpy_letter, first_whitespace, cmpy_number, cmpy_desc, next_cmpy_letter, second_whitespace, next_cmpy_number) in re.findall(regex, pdf_text, re.DOTALL):
        # cmpy_code = (cmpy_letter +  cmpy_number).strip()
        cmpy_code = cmpy_code.strip()
        # print cmpy_code
        split_desc = cmpy_desc.split(',')
        cmpy_name = split_desc[0].strip()
        # print cmpy_code, "\t", cmpy_name
        if len(split_desc) < 2:
            print cmpy_desc
            print "There is no comma in this company"
        else:
            if ("inc" in split_desc[1].lower()):
                split_desc.remove(split_desc[1])
            cmpy_address = ",".join(split_desc[1:])
            regex_zip = "(.*?)(\d{5})"
            cmpy_address_without_zip =  re.findall(regex_zip, cmpy_address, re.DOTALL)[0][0]
            zip = re.findall(regex_zip, cmpy_address, re.DOTALL)[0][1].strip()
            cmpy_address_list = cmpy_address_without_zip.split(',')
            cmpy_city = cmpy_address_list[len(cmpy_address_list) - 2].strip()
            cmpy_state = cmpy_address_list[len(cmpy_address_list) - 1].strip()
            regex_facilities = "(\.)(\s*)([1-9]+)"
            cmpy_facilities = re.findall(regex_facilities, cmpy_desc)
            # print cmpy_desc
            print cmpy_code, "\t", cmpy_name, "\t", zip, "\t", cmpy_city, "\t", cmpy_state
            num_facilities = len(cmpy_facilities)
            if len(cmpy_facilities) > 0:
                last_facility = cmpy_facilities[len(cmpy_facilities) - 1]
                last_facility_number = int(last_facility[2])
                print "Last facility number = ", last_facility_number
                if last_facility_number > len(cmpy_facilities):
                    num_facilities = last_facility_number
            print "Number of facilities = ", num_facilities
            dash_regex = "-+[A-Z]"
            dash_list = re.findall(dash_regex, cmpy_desc)
            # print "Another number = ", len(dash_list)
            # regex_professional = "[?<=[P[\s*]r[\s*]o[\s*]f[\s*]e[\s*]s[\s*]s[\s*]i[\s*]o[\s*]n[\s*]a[\s*]l[\s*]S[\s*]t[\s*]a[\s*]f[\s*]f[\s*]:[\s*]][\d]+"
            regex_professional = "(P\s*r\s*o\s*f\s*e\s*s\s*s\s*i\s*o\s*n\s*a\s*l\s*S\s*t\s*a\s*f\s*f\s*:\s*)(\d+)"
            professionals_list = re.findall(regex_professional, cmpy_desc)
            for professionals in professionals_list:
                print "Professional Staff: ", professionals[1]
            regex_doctorates = "(D\s*o\s*c\s*t\s*o\s*r\s*a\s*t\s*e\s*s\s*:\s*)(\d+)"
            doctorates_list = re.findall(regex_doctorates, cmpy_desc)
            for doctorates in doctorates_list:
                print "Doctorates: ", doctorates[1]
            regex_technicians = "(T\s*e\s*c\s*h\s*n\s*i\s*c\s*i\s*a\s*n\s*s\s*&\s*A\s*u\s*x\s*i\s*l\s*i\s*a\s*r\s*i\s*e\s*s\s*:\s*)(\d+)"
            technicians_list = re.findall(regex_technicians, cmpy_desc)
            for technician in technicians_list:
                print "Technicians & Auxiliaries: ", technician[1]
            regex_activity = "\(\s*(?:p|g|i|c|P|G|I|C)+\s*(?:p|g|i|c|P|G|I|C)?\s*(?:p|g|i|c|P|G|I|C)?\s*(?:p|g|i|c|P|G|I|C)?\s*\)"
            activity_list = re.findall(regex_activity, cmpy_desc)
            for activity_code in activity_list:
                print "R&D activity code - ", activity_code
            raw_input("Press Enter to continue...")


    # print m.group()
    # print pdf_text