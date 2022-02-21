from news.models import *
#1
user1 = User.objects.create_user('Kate')
user2 = User.objects.create_user('Den')

#2
auth1 = Author.objects.create(user=user1)
auth2 = Author.objects.create(user=user2)

#3
cat1 = Category.objects.create(name='Спорт')
cat2 = Category.objects.create(name='Погода')
cat3 = Category.objects.create(name='Здоровье')
cat4 = Category.objects.create(name='Еда')

#4
head1 = 'У сборной России еще одна медаль'
text1 = """Только что в Пекине (Китай) на арене «Центральный» завершился \
финальный матч мужского олимпийского турнира по хоккею, в котором встречались \
сборные России и Финляндии. Встреча завершилась победой финнов со счётом 2:1. \
Таким образом, Россия завоевала еще одну медаль - серебряную."""
head2 = 'Овсяные блинчики с бананом'
text2 = """Время приготовления 20 минут
 Калорийность 155 ккал/100 г
 Ингредиенты (2 порции)
 - банан – 1 шт;
 - овсяные хлопья (быстрого приготовления) – 4 ст. л;
 - яйцо – 1 шт;
 - растительное масло – 1 ч. л;
 - соль – по вкусу;
 - молоко – 60 мл."""
head3 = 'Гололед в Питере'
text3 = """Погодные условия в Петербурге продолжают портить жизнь гостям и \
местным жителям: в городе снова объявили «желтый» уровень опасности. В этот раз \
причиной стал гололед и мокрый снег."""

p1 = Post.objects.create(author=auth2, type='NWS', head=head1, text=text1)
p2 = Post.objects.create(author=auth1, type='ART', head=head2, text=text2)
p3 = Post.objects.create(author=auth2, type='ART', head=head3, text=text3)

#5
p1.category.add(cat1)
p2.category.add(cat3, cat4)
p3.category.add(cat2)

#6
c1 = Comment.objects.create(post=p1, author=user1, text='Какие молодцы!')
c2 = Comment.objects.create(post=p2, author=user2, text='Сделал. Не понравились, не сладко')
c3 = Comment.objects.create(post=p3, author=user1, text='Да уж... Такое по всему городу')
c4 = Comment.objects.create(post=p2, author=user1, text='Попробуйте с медом')
c5 = Comment.objects.create(post=p3, author=user1, text='И не только в Питере')

#7
p1.like()
p1.like()
p2.like()
p2.dislike()
p2.like()
p3.dislike()
p3.dislike()
p3.like()
c1.like()
c2.like()
c2.dislike()
c3.like()
c3.like()
c4.like()

#8
auth1.update_rating()
auth2.update_rating()

#9
Author.objects.all().order_by('-rating').values('user__username', 'rating')[0]
#or
best_auth = Author.objects.all().order_by('-rating')[0]
'best_auth: ' + 'username: ' + best_auth.user.username + ', rating: ' + str(best_auth.rating)

#10
best_art = Post.objects.filter(type='ART').order_by('-rating')[0]
'best_art: ' + 'date_in: ' + best_art.time_in.strftime('%d.%m.%Y') + ', username: ' + best_art.author.user.username + ', rating: ' + str(best_art.rating) + ', head: ' + best_art.head
best_art.preview()

#11
Comment.objects.filter(post=best_art).values('time_in', 'author__username', 'rating', 'text')
