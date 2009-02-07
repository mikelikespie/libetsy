from etsy import Etsy

e = Etsy("YOUR API KEY HERE")

# get my User object:
me = e.getUserDetails('muffinshop')

print "people who favor %s" % me.user_name
print

#iterate through people that favorite me:
for f in me.getFavorers():
    if f.status != 'private':
        print f.user_name

print
print "%s's listings" % me.user_name
print
#get my shop
s = me.getShopDetails()

#iterate through my listings
for l in s.getListings():
    print l.title

