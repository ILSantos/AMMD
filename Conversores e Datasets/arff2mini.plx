#!/usr/bin/perl

# Converte um arquivo ARFF em formato MiniARFF.
# Modo de uso: miniarff.plx <entrada> <saida>
#
# Rafael Giusti
# rfgiusti@gmail.com
# 2019-05-18
# 
# Instruções
#    Utilize através da linha de comando. É necessário Perl 5 para execução do script (recomendado 5.28)
#
#    O arquivo de entrada deve ser no formato ARFF, respeitando as seguintes limitações:
#    * apenas atributos numéricos e categóricos
#    * nomes de atributos e valores de atributos devem ser simples (uma única palavra, sem aspas)
#    * não são aceitos arquivos ARFF esparsos
#
# Para converter arquivos CSV ou arquivos (names,data) em MiniARFF, converta manualmente os dados para ARFF
# acrescentando informações sobre os atributos. Teste o arquivo ARFF tentando carregá-lo no Weka antes de
# realizar a conversão.
#
# Este script apenas converte os dados, não verificando se o arquivo ARFF é válido.

use strict;

my $in = $ARGV[0];
my $out = $ARGV[1];

die "Uso: $0 <entrada> <saida>\n" unless defined $in;
die "Uso: $0 <entrada> <saida>\n" unless defined $out;

die "Nao e' possivel ler ou encontrar o arquivo de entrada '$in'\n" unless (-f $in && -r $in);

my @features = ();
my $class = -1;
my @data;
my %featurenames;

my $databegin = 0;

open IN, "$in" or die "Nao foi possivel abrir o arquivo de entrada '$in'\n";
while (my $line = <IN>) {
	die "Erro de leitura: $!\n" unless defined $line;

	# Remove comentários e espaços em branco no começo da linha
	chomp $line;
	$line =~ s/^\s*(%.*)?//;
		
	# Nomes e valores com aspas não são aceitos pelo conversor
	die "Erro: Nomes e valores com aspas nao sao aceitos pelo conversor\n" .
			"Leitura interrompida na linha $. do arquivo '$in':\n" .
			"$line\n" if $line =~ /["']/;

	# Em que parte estamos? Nomes ou dados?
	if ($databegin) {
		push @data, $line;
	}
	else {
		# Ignora o nome da relação e linhas vazias
		if ($line =~ /^\@RELATION/i || $line =~ /^\s*$/) {
			next;
		}

		# É um atributo ou o começo dos dados?
		if ($line =~ s/^\@ATTRIBUTE\s+//i) {
			# Qual é o nome do atributo?
			$line =~ s/[-a-zA-Z0-9_+]+// or die "Erro: nome de atributo invalido na linha $. do arquivo '$in'\n";
			my $fname = $&;
			my $ftype;
			my @fvalues;

			# O nome do atributo é "class"?
			if ($fname =~ /class/i) {
				print "Possivel atributo classe encontrado (atributo '$fname', $in, linha $.)\n";
				$class = scalar(@features);
			}

			# O nome do atributo é repetido?
			die "Erro: atributo '$fname' declarado duas ou mais vezes ($in, linha $.)\n" if defined $featurenames{$fname};
			$featurenames{$fname} = 1;

			# Qual é o tipo do atributo?
			if ($line =~ /^\s*NUMERIC/i) {
				$ftype = "num";
				@fvalues = ();
			}
			elsif ($line =~ /^\s*{\s*(.*)\s*}/) {
				my $cat = $1;
				$cat =~ s/\s*,\s*/,/g;
				die "Erro: categorias contem espacos (atributo '$fname', $in, linha $.)\n" if $cat =~ /\s/;
				die "Erro: categorias invalidas (atributo '$fname', $in, linha $.): $cat\n" if $cat =~ /[^-a-zA-Z0-9+_,]/;

				$ftype = "cat";
				@fvalues = split /,/, $cat;
			}
			elsif ($line =~ /^\s*DATE/i) {
				die "Erro: atributos do tipo 'DATE' nao sao suportados (atributo '$fname', $in, linha $.)\n"
						. "Converta as datas para timestamps e o atributo em numerico.\n";
			}
			elsif ($line =~ /^s*STRING/i) {
				die "Erro: atributos do tipo 'STRING' nao sao suportados (atributo '$fname', $in, linha $.)\n"
						. "Converta o atributo em categorias.\n";
			}
			else {
				die "Erro: atributo de tipo invalido (atributo '$fname', $in, linha $.)\n"
						. "Atributos suportados sao categoricos e numericos.\n";
			}

			print "Atributo encontrado: $fname ($ftype)";
			if ($ftype eq "cat") {
				print " -- " . join(", ", @fvalues);
			}
			print "\n";
			push @features, {name => $fname, type => $ftype, values => [@fvalues]};
		}
		elsif ($line =~ s/^\@DATA\s*//i) {
			$databegin = 1;
			print "Dados encontrados. Lendo exemplos...\n";
		}
		else {
			die "Erro lendo o arquivo '$in'. A linha $. nao e' suportada pelo conversor:\n" .
			"$line\n";
		}
	}
}
close IN;

# Alguns testes simples...
die "Erro: nenhum atributo encontrado no arquivo '$in'!\n" unless @features;
die "Erro: nao foram encontrados dados no arquivo '$in'!\n" unless @data;
print "Encontrados " . (scalar @data) . " exemplos\n";

$class = $#features unless $class >= 0;
my $classname = $features[$class]->{name};
print "Assumindo o atributo '$classname' como a classe\n";
if ($class != $#features) {
	print "Os atributos serao reordenados para que a classe fique no final\n";
}

print "Escrevendo arquivo Mini ARFF '$out'...\n";

# Começa a construir o arquivo
open OUT, ">$out" or die "Erro: nao foi possivel abrir o arquivo '$out'\n";

# Número de atributos primeiro...
my $numfeatures = scalar(@features) - 1;
print OUT "$numfeatures\n";

# Descreve os atributos, deixando a classe para o final
# O jeito mais simples é duplicar o atributo classe e pular a primeira ocorrência
push @features, $features[$class];
my $skippedClass = 0;
foreach my $feat (@features) {
	if ($feat->{name} eq $classname) {
		if (!$skippedClass) {
			# Ignora a classe uma vez
			$skippedClass = 1;
			next;
		}
		else {
			# Imprime o indicativo de que temos uma classe para depois descrever a classe
			print OUT "1\n";
		}
	}
	
	if ($feat->{type} eq "num") {
		print OUT "num $feat->{name}\n" or die "$!";
	}
	else {
		my @cat = @{$feat->{values}};
		my $numcat = scalar @cat;
		print OUT "cat $feat->{name} $numcat " . join(" ", @cat) . "\n" or die "$!";
	}
}

# Imprime o número de exemplos
print OUT scalar(@data) . "\n";

# Imprime os exemplos, separando por espaços e deixando a classe no final
for my $datum (@data) {
	# Remove espaços no início, no fim e entre vírgulas; se sobrarem espaços, é erro
	$datum =~ s/^\s*//;
	$datum =~ s/\s*$//;
	$datum =~ s/\s*,\s*/,/g;

	my @values = split /,/, $datum;
	print OUT join(" ", @values[0 .. $class - 1], @values[$class + 1 .. $#values], $values[$class]) . "\n" or die "$!";
}

close OUT;

print "Sucesso\n";
